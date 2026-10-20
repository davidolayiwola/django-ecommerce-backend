# built in module
from rest_framework.views import APIView
from rest_framework import status, generics, viewsets
from rest_framework.response import Response
# from rest_framework import generics
# from rest_framework import viewset
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication

from rest_framework import filters
from rest_framework.pagination import PageNumberPagination

from rest_framework import serializers


# from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

# from datetime import datetime
# from django.shortcuts import get_object_or_404

# Model classes
from .models import CustomUser, ProductModel, CategoryModel, CartModel
from .models import CartItemModel, OrderModel, OrderItemModel

# Serializer classes
from .serializers import UserSerializer, CreateProductSerializer, ProductSerializer
from .serializers import CategorySerializer, CartSerializer, CartItemSerializer
from .serializers import OrderSerializer, OrderItemSerializer

# Permission classes
from .permission_class import IsOwnerOrAdminUser, IsCartOwner, IsOwner



"""

    User Views

"""
class UserCreateView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """Create a new user"""
        email = request.data.get("email")
        password = request.data.get("password")

        # Returns Custom user instance
        user = authenticate(email=email, password=password)

        if user:
            # Returns Token instance
            token, created = Token.objects.get_or_create(user=user)

            return Response({'id': user.id,'email': user.email, 'token': token.key})

        else:
            return Response({'error': 'Wrong credentials'}, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # print(f"Token is {request.user.auth_token.key}")

        request.user.auth_token.delete()

        return Response(status=status.HTTP_200_OK)


class ListUsers(generics.ListAPIView):
    """Get all users"""
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, IsAdminUser]

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination

    """
        Allow User full-text searches on a queryset based on the provided search terms
        Using the url sample: api/v1/users/?search=david.

        Users can also order queryset by using the url below
        url: api/v1/users/?ordering=first_name
    """
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    # Specify fields to be used for search and ordering
    search_fields = ['email', 'first_name', 'last_name']
    ordering_fields = ['first_name', 'last_name']


    """
        set this attribute or override the get_queryset() method
        as queryset will get evaluated once and those
        results will be cached for all subsequent requests.
    """
    def get_queryset(self):
        # Customize the queryset here, e.g., apply filters or annotations
        return CustomUser.objects.filter(is_active=True).order_by("first_name")


class RetrieveUser(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, IsOwnerOrAdminUser]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    # lookup_field = "first_name" # defaults to id
    # lookup_url_kwargs = "first_name" # defaults to lookup_field value


    """
        override the get_object method by calling the .check_object_permissions(request, obj) 
        method at the point at which you’ve retrieved the object.
    """
    def get_object(self):
        #  perform additional filtering on the queryset based on the request parameters. 
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {
            self.lookup_field: self.kwargs[self.lookup_field] # Assuming URL pattern captures 'title'
        }

        obj = generics.get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)

        return obj


class UpdateUser(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, IsOwnerOrAdminUser]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class RemoveUser(generics.DestroyAPIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, IsOwnerOrAdminUser]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()

        return Response(
            {"detail": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


"""

    Product Views

"""

class CreateProduct(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = CreateProductSerializer


class ListProducts(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    pagination_class = PageNumberPagination

    search_fields = ["name", "brand",]
    ordering_fields = ["name", "release_date"]

    def get_queryset(self):
        return ProductModel.objects.all().order_by("-release_date")


class RetrieveProduct(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer


class UpdateProduct(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer


class RemoveProduct(generics.DestroyAPIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()

        return Response({'message': "Producted successfully deleted"}, status=status.HTTP_204_NO_CONTENT)


"""

    Cart Views

"""

class ListCarts(generics.ListAPIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, IsAdminUser]

    queryset = CartModel.objects.all()
    serializer_class = CartSerializer
    pagination_class = PageNumberPagination

    filter_backends = [filters.SearchFilter, ]
    search_fields = ["created_at"]

    def get_queryset(self):
        return CartModel.objects.all().order_by("-created_at")


# class CreateCart(generics.CreateAPIView):
#     authentication_classes = [TokenAuthentication, ]
#     permission_classes = [IsAuthenticated]
#     serializer_class = CartSerializer

#     def perform_create(self, serializer):
#         # Check a user has a cart before creating a new one
#         queryset = CartModel.objects.filter(user=self.request.user)

#         if queryset.exists():
#             # raise serializers.ValidationError('You have already created a cart')
#             return

#         serializer.save()

#     # def post(self, request, *args, **kwargs):
#     #     return self.create(request, *args, **kwargs)



class RetrieveRemoveCart(generics.RetrieveDestroyAPIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, IsAdminUser] # allow authenticated admin only
    queryset = CartModel.objects.all()
    serializer_class = CartSerializer

    # def get_object(self):
    #     #  perform additional filtering on the queryset based on the request parameters. 
    #     queryset = self.filter_queryset(self.get_queryset())
    #     filter_kwargs = {
    #         self.lookup_field: self.kwargs[self.lookup_field] # Assuming URL pattern captures 'title'
    #     }

    #     obj = generics.get_object_or_404(queryset, **filter_kwargs)
    #     self.check_object_permissions(self.request, obj)

    #     return obj




# class RemoveCart(generics.DestroyAPIView):
#     authentication_classes = [TokenAuthentication, ]
#     permission_classes = [IsAuthenticated, IsAdminUser]
#     queryset = CartModel.objects.all()
#     serializer_class = CartSerializer

#     def delete(self, request, *args, **kwargs):
#         instance = self.get_object()
#         instance.delete()

#         return Response({'message': 'Cart successfully deleted'}, status=status.HTTP_204_NO_CONTENT)



"""

    CartItem Views

"""

class CreateCartItem(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]
    # serializer_class = CartItemSerializer

    def post(self, request):
        
        def add_new_cartitem(data):
            cart_item = CartItemSerializer(data=data)
            cart_item.is_valid(raise_exception=True)
            cart_item.save()

        try: 
            # Check if the user has a cart created already
            user_cart = CartModel.objects.get(user=request.user)
            product = CartItemModel.objects.filter(product=request.data.get("product"))

            # Check if product  already exist in cart
            if product.exists():
                return Response({'message': "Product already exit in cart"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                data = request.data
                data["cart"] = user_cart.id
                add_new_cartitem(data)

                return Response({'message': "Product successfully added"}, status=status.HTTP_201_CREATED)
    
        except CartModel.DoesNotExist:
            new_cart = CartSerializer(data={"user":request.user.id})
            new_cart.is_valid(raise_exception=True)
            saved_cart = new_cart.save()

            data = request.data
            data["cart"] = saved_cart.id
            add_new_cartitem(data)

            return Response({'message': "Product successfully added"}, status=status.HTTP_201_CREATED)


class ListCartItems(generics.ListAPIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ] 
    queryset = CartItemModel.objects.all()
    serializer_class = CartItemSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        try: 
            cart = CartModel.objects.get(user=self.request.user)
            return CartItemModel.objects.filter(cart=cart.id)
        except CartModel.DoesNotExist:
            return []



class AdminListCartItems(generics.ListAPIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = CartItemModel.objects.all()
    serializer_class = CartItemSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        # print(f"Hello, it is {self.kwargs["pk"]}")
        return CartItemModel.objects.filter(cart=self.kwargs["pk"])


class UpdateCartItem(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, IsCartOwner]

    def put(self, request, cart_pk, pk):
        # cart = CartModel.objects.get(user=self.request.user) 

        data = request.data
        data["cart"] = cart_pk

        try:
            cart_item = CartItemModel.objects.get(pk=pk)

            # serialised_data = CartItemSerializer(data=data)
            serialised_data = CartItemSerializer(cart_item, data)

            if serialised_data.is_valid():
                saved_data = serialised_data.save()
                return Response({"message":"Cart item successfully updated"}, status=status.HTTP_200_OK)
            else:
                return Response({"message":serialised_data.errors}, status=status.HTTP_400_BAD_REQUEST)
        except CartItemModel.DoesNotExist:
            return Response({"message": "Item to be updated not found"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, cart_pk, pk):
        # cart = CartModel.objects.get(user=self.request.user) 

        data = request.data
        data["cart"] = cart_pk

        try:
            cart_item = CartItemModel.objects.get(pk=pk)

            # serialised_data = CartItemSerializer(data=data)
            serialised_data = CartItemSerializer(cart_item, data, partial=True)

            if serialised_data.is_valid():
                saved_data = serialised_data.save()
                return Response({"message":"Cart item successfully updated"}, status=status.HTTP_200_OK)
            else:
                return Response({"message":serialised_data.errors}, status=status.HTTP_400_BAD_REQUEST)
        except CartItemModel.DoesNotExist:
            return Response({"message": "Item to be updated not found"}, status=status.HTTP_404_NOT_FOUND)

class RemoveCartItem(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, IsCartOwner]

    def delete(self, request, cart_pk, pk):
        try:
            cart_item = CartItemModel.objects.get(pk=pk)
            cart_item.delete()
            return Response({"message": "Item deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        except CartItemModel.DoesNotExist:
            return Response({"message": "Item not found"}, status=status.HTTP_404_NOT_FOUND)


"""

    Order Views

"""
class CreateOrder(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    serializer_class = OrderSerializer

    # def post(self, request):
    #     data = request.data
    #     data["user"] = request.user.id

    #     serialised_data = OrderSerializer(data=data)

    #     if serialised_data.is_valid():
    #         saved_order = serialised_data.save()
    #         return Response({"message": "Order successfully placed"}, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(serialised_data.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminListOrders(generics.ListAPIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, IsAdminUser]

    serializer_class = OrderSerializer
    pagination_class = PageNumberPagination

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    search_fields = ['created_at', 'user', 'transaction_id']
    ordering_fields  = ['created_at']

    def get_queryset(self):
        return OrderModel.objects.all().order_by("-created_at")


class ListOrdersByOwner(generics.ListAPIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ] 
    queryset = OrderModel.objects.all()
    serializer_class = OrderSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        if OrderModel.objects.filter(user=self.request.user).exists(): 
            return OrderModel.objects.filter(user=self.request.user)
        else:
            return []


class RetrieveRemoveOrder(generics.RetrieveDestroyAPIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, IsOwnerOrAdminUser]
    queryset = OrderModel.objects.all()
    serializer_class = OrderSerializer

class UpdateOrder(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = OrderModel.objects.all()
    serializer_class = OrderSerializer


"""

    OrderItem Views

"""
class OrderItemViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication ]
    permission_classes = [IsAdminUser]

    queryset = OrderItemModel.objects.all()
    serializer_class = OrderItemSerializer
    pagination_class = PageNumberPagination


"""

    Category Views

"""
class CategoryViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication ]
    permission_classes = [IsAdminUser]

    queryset = CategoryModel.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination



