from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.contrib import messages
from .models import *
from .forms import *
from django.utils import timezone
from datetime import timedelta

User  = get_user_model()

def login_view(request):

    if request.method == "POST":

        email = request.POST.get('email')
        password = request.POST.get('password')

        if request.session.get("block_time"):

            block_time = timezone.datetime.fromisoformat(request.session["block_time"])

            if timezone.now() < block_time:

                time_left = block_time - timezone.now()
                messages.error(request, f"Too many unsusscessful attempts,  try again in {time_left.seconds // 60} minutes")
                return redirect('login')

        if not request.session.get("failed_attempts"):

            request.session["failed_attempts"] = 0
            request.session["first_failed_attempt_time"] = str(timezone.now())

        first_failed_attempt_time = timezone.datetime.fromisoformat(request.session["first_failed_attempt_time"])
        
        if timezone.now() - first_failed_attempt_time > timedelta(minutes=5) :

            request.session["failed_attempts"] = 0
            request.session["first_failed_attempt_time"] = str(timezone.now())

        if request.session["failed_attempts"] >= 3:

            if not request.session.get("block_time"):

                request.session["block_time"] = str(timezone.now() + timedelta(minutes=10) )

            return redirect('login')

        user = authenticate(request, username=email, password=password)

        if user is not None:

            login(request, user)
            request.session["failed_attempts"] = 0

            if user.is_superuser:

                return redirect('/admin/')

            return redirect('products') 
        
        else:

            request.session["failed_attempts"] += 1
            messages.error(request, "Invalid email or password")

    return render(request, "login.html")

def signup_view(request):

    if request.method == "POST":

        form = UserSignupForm(request.POST)

        if form.is_valid():

            form.save()
            messages.success(request, "Account created successfully! Please log in :)")
            return redirect("login")
        
        else:

            messages.error(request, "Please correct the errors below:")

    else:

        form = UserSignupForm()

    return render(request, "signup.html", {"form": form})

def products_view(request):

    products = Product.objects.all()
    return render(request, "products.html", {"products": products})

def basket_view(request):

    if request.user.is_authenticated:

        basket = Basket.objects.get_or_create(user=request.user)[0]
        basket_items = BasketItem.objects.filter(basket=basket)
        products_in_basket = []
        basket_total = 0

        for basket_item in basket_items:
            product = basket_item.product
            quantity = basket_item.quantity
            total_price = product.price * quantity
            basket_total += total_price

            products_in_basket.append({

                'product': product,
                'quantity': quantity,
                'total_price': total_price,
                'basket_item': basket_item 
            })

        return render(request, "basket.html", {'products_in_basket': products_in_basket, 'basket_total': basket_total})

    else:

        return redirect('login')

def checkout_view(request):

    if not request.user.is_authenticated:

        return redirect('login')  
    
    basket = get_object_or_404(Basket, user=request.user)
    basket_items = BasketItem.objects.filter(basket=basket)

    if not basket_items.exists():

        messages.error(request, "Your basket is empty!")
        return redirect('products')

    for item in basket_items:
        
        if item.quantity > item.product.stock:

            messages.error(request, f"Not enough stock for {item.product.name}.")
            return redirect('basket')

    if request.method == 'POST':

        delivery_form = DeliveryAddressForm(request.POST)
        payment_form = PaymentDetailForm(request.POST)

        if delivery_form.is_valid() and payment_form.is_valid():

            delivery_address = delivery_form.save(commit=False)
            delivery_address.user = request.user
            delivery_address.save()

            payment_detail = payment_form.save(commit=False)
            payment_detail.user = request.user
            payment_detail.save()

            order = Order.objects.create(

                user=request.user,
                status='Pending',
                delivery_address=delivery_address,
                payment_detail=payment_detail,
                total_price=sum(item.quantity * item.product.price for item in basket_items)

            )

            for item in basket_items:

                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price_at_purchase=item.product.price

                )

                item.product.stock -= item.quantity 
                item.product.save()

            basket_items.delete()

            messages.success(request, "Your order has been placed successfully")
            return redirect('orders')

        else:

            messages.error(request, "Your order was unsucessful")

    else:

        delivery_form = DeliveryAddressForm()
        payment_form = PaymentDetailForm()

    return render(request, 'checkout.html', {
        'delivery_form': delivery_form,
        'payment_form': payment_form,
        'basket_items': basket_items
    })

def orders_view(request):

    if request.user.is_authenticated:

        orders = Order.objects.filter(user=request.user)

        for order in orders:

            order.payment_detail.last_four_digits = order.payment_detail.accountnumber[-4:]

        paginator = Paginator(orders, 10) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'orders.html', {'page_obj': page_obj})
    
    else:

        messages.error(request, "You must be logged in to view your orders")
        return redirect('login')

def add_to_basket(request, product_id):

    if request.method == "POST":

        product = Product.objects.get(id=product_id)
        
        try:

            quantity = int(request.POST.get('quantity', 1))

        except ValueError:

            quantity = 1 
        
        if request.user.is_authenticated:

            basket, created = Basket.objects.get_or_create(user=request.user)
        
            basket_item, created = BasketItem.objects.get_or_create(

                basket=basket, product=product,
                defaults={'quantity': quantity} 

            )
            
            if not created: 

                basket_item.quantity += quantity
                basket_item.save()
            
            messages.success(request, f"{quantity} x {product.name} added to your basket")

        else:

            messages.error(request, "You need to be logged in to add items to your basket.")
        
        return redirect('products')
    
def remove_from_basket(request, item_id):
 
    if request.method == "POST":

        basket_item = get_object_or_404(BasketItem, id=item_id, basket__user=request.user)
        basket_item.delete()
        messages.success(request, "Product removed from basket!")

    return redirect("basket")
    
def logout_view(request):

    logout(request)
    return redirect('login')