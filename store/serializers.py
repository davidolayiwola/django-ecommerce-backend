from rest_framework import serializers
from django.core.validators import MinValueValidator

from .models import CustomUser, ProductModel, CategoryModel, CartModel
from .models import CartItemModel, OrderModel, OrderItemModel


class UserSerializer(serializers.ModelSerializer):
    """Serializers CustomUser model"""
  
    """
        ModelSerialer methods that can be overriden
            1. create()
            2. update()
            3. validate()
            4. save() - don't override this
    """

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'is_staff',
            'password'
        ]
        # fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}, # Don't expose user's password
            'is_staff': {'write_only': True}, # Don't expose user's role
        }


    def create(self, validated_data):
        """Create a custom User using the create_user()"""

        # Remove password
        password = validated_data.pop("password")
        email = validated_data.pop("email")

        user = CustomUser.objects.create_user(email, password, **validated_data)

        return user


    def update(self, instance, validated_data):
        # Remove password
        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)
        
        instance.save()

        return instance


class CreateProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProductModel
        fields = '__all__'
        extra_kwargs = {
            "price": {"validators": [MinValueValidator(0.0)]},
            "quantity": {"validators": [MinValueValidator(0)]}
        }

class ProductSerializer(serializers.ModelSerializer):
    """
        Customize serializer to return category as sting and not id
    """
    category = serializers.StringRelatedField()

    class Meta:
        model = ProductModel
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartModel
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItemModel
        # fields = ['product', 'quantity']
        fields = '__all__'



class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderModel
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItemModel
        fields = '__all__'

 