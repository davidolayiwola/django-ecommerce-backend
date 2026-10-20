from django.db import models

import uuid

"""
Import django's core authentication building block
    - AbstractBaseUser provides core auth logic like password hashing without default fields
    - BaseUserManager provides helper methods to create users and superusers
    - PermissionsMixin adds django permission and group management fields
"""

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Base class to create a custom user
class CustomUserManager(BaseUserManager):

    # Create a custom user
    def create_user(self, email, password=None, **extra_fields):
        if not email: # Check if email is not null
            raise ValueError("The email field is required")

        # Standadize email adddress e.g taking User@DOMain.com to User@domain.com
        email = self.normalize_email(email) 

        # Create user using the model method from the super class
        user = self.model(email=email, **extra_fields)
        user.set_password(password) # Hash and set password

        # Save user in db ensuring compatibility with multi-database setups
        user.save(using=self._db) 

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):

    # Define table fields
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    """
        Link CustomUserManager to CustomUser
        Make CustomUserManager the interface for db queries and user creation
    """
    objects = CustomUserManager()

    # Instruct django to use email as unique identifier
    USERNAME_FIELD = 'email'

    """
        Specify additional fields that must be provided when creating suoeruser vai the terminal
        Email and password are required by default
    """
    REQUIRED_FIELDS = ['first_name']

    def __str__(self):
        return self.email
        

class CategoryModel(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class ProductModel(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=50)
    brand = models.CharField(max_length=30)
    price = models.FloatField(default=0)
    quantity = models.IntegerField(default=0)
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)
    release_date = models.DateField()

    def __str__(self):
        return self.name


class CartModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Cart " + str(self.id)


class CartItemModel(models.Model):
    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    # add_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "CartItem " + str(self.id)


def generate_transaction_id():
    return uuid.uuid4().hex
    

class OrderModel(models.Model):
    transaction_status = (
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered")
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_price = models.FloatField(default=0)
    status = models.CharField(
        max_length=10,
        choices=transaction_status,
        default="pending"
    )
    shipping_address = models.CharField(max_length=100)
    transaction_id = models.CharField(
        max_length=32,
        default=generate_transaction_id, 
        unique=True, 
        editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True) # default="2026-09-26 14:31:10.897033")

    def __str__(self):
        return "Order " + str(self.id)


class OrderItemModel(models.Model):
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    price_at_purchase = models.FloatField(default=0)

    def __str__(self):
        return "OrderItem " + str(self.id)

