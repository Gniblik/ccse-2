from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from encrypted_model_fields.fields import *
from django.utils.timezone import now

class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):

        if not email:

            raise ValueError('The Email field must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:

            raise ValueError('Superuser must have is_staff=True.')
        
        if extra_fields.get('is_superuser') is not True:

            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):

    first_name = EncryptedCharField(max_length=150, blank=False)
    last_name = EncryptedCharField(max_length=150, blank=False)
    email = models.EmailField(unique=True)
    phone_number = EncryptedCharField(max_length=15, blank=True, null=True)
    is_staff = EncryptedBooleanField(default=False)
    is_active = EncryptedBooleanField(default=True)
    date_joined = models.DateTimeField(default=now)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):

        return self.email

class Product(models.Model):

    name = EncryptedCharField(max_length=50, null=False, unique=True)
    price = models.DecimalField(decimal_places=2, null=False, max_digits=13)
    description = EncryptedCharField(max_length=2000, null=False)
    stock = EncryptedIntegerField(null=False, default=0)
    image = models.ImageField(upload_to="product_images/", )

    def __str__(self):

        return self.name

class Basket(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class BasketItem(models.Model):

    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = EncryptedIntegerField(null=False)

class DeliveryAddress(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = EncryptedCharField(max_length=50, null=False)
    address_2 = EncryptedCharField(max_length=50, null=True)
    region = EncryptedCharField(max_length=50, null=False)
    postcode = EncryptedCharField(max_length=10, null=False)

class PaymentDetail(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    accountnumber = EncryptedCharField(max_length=20, null=False)
    expiration_date = EncryptedCharField(max_length=5, null=False)
    cvc = EncryptedCharField(max_length=3, null=False)

class Order(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class OrderStatus(models.TextChoices):
        PENDING = 'Pending'
        COMPLETED = 'Completed'
        SHIPPED = 'Shipped'

    status = models.CharField(max_length=50, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    delivery_address = models.ForeignKey(DeliveryAddress, on_delete=models.CASCADE, default=1)
    payment_detail = models.ForeignKey(PaymentDetail, on_delete=models.CASCADE, default=1)
    total_price = models.DecimalField(max_digits=16, null=False, decimal_places=2)

class OrderItem(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = EncryptedIntegerField(null=False)
    price_at_purchase = models.DecimalField(decimal_places=2, null=False, max_digits=13)
