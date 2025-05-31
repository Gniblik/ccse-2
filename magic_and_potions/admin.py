from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ("name", "price", "stock")
    list_filter = ("price",)
    search_fields = ("name", "description")

@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):

    list_display = ("user",)

@admin.register(BasketItem)
class BasketItemAdmin(admin.ModelAdmin):

    list_display = ("basket", "product", "quantity")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = ("user", "status", "total_price")
    list_filter = ("status",)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = ("order", "product", "quantity", "price_at_purchase")

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    model = CustomUser
    list_display = ("email", "first_name", "last_name", "is_staff")
    ordering = ("email",)

    fieldsets = (

        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "phone_number")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "first_name", "last_name", "phone_number"),
        }),
    )

    search_fields = ("email", "first_name", "last_name")

@admin.register(DeliveryAddress)
class DeliveryAddressAdmin(admin.ModelAdmin):

    model = DeliveryAddress
    list_display = ("address", "address_2", "region", "postcode")

@admin.register(PaymentDetail)
class PaymentAdmin(admin.ModelAdmin):
    
    model = PaymentDetail
    list_display = ()