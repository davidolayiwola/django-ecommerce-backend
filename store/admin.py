from django.contrib import admin

from .models import CustomUser, CategoryModel, ProductModel
from .models import CartModel, CartItemModel, OrderModel, OrderItemModel

# Register your models here.
admin.site.register(CategoryModel)
@admin.register(ProductModel)
class ProductAdminModel(admin.ModelAdmin):
    """Display the fields in the tupe below"""
    list_display = ("id", "name", "description", "quantity", "price", "category", "release_date")

@admin.register(CustomUser)
class CustomUserModelAdmin(admin.ModelAdmin):
    """Display the fields in the tupe below"""
    list_display = ("id", "email", "first_name")

@admin.register(CartModel)
class CartModelAdmin(admin.ModelAdmin):
    """Display the fields in the tupe below"""
    list_display = ("id", "user", "created_at")

@admin.register(CartItemModel)
class CartItemModelAdmin(admin.ModelAdmin):
    """Display the fields in the tupe below"""
    list_display = ("id", "cart", "product", "quantity")

@admin.register(OrderModel)
class OrderModelAdmin(admin.ModelAdmin):
    """Dis the fields below"""
    list_display = ("id", "user", "transaction_id", "total_price", "created_at", "status")
    
admin.site.register(OrderItemModel)
