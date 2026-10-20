# Built in classes
from django.urls import path
from rest_framework.routers import DefaultRouter

# View classes
from .views import ListUsers, UserCreateView, UserLoginView, UserLogoutView
from .views import RetrieveUser, UpdateUser, RemoveUser

from .views import CategoryViewSet
from .views import OrderItemViewSet

from .views import CreateProduct, ListProducts, RetrieveProduct
from .views import UpdateProduct, RemoveProduct

from .views import ListCarts, RetrieveRemoveCart # CreateCart 
from .views import CreateCartItem, ListCartItems, AdminListCartItems, UpdateCartItem, RemoveCartItem

from .views import CreateOrder, AdminListOrders, ListOrdersByOwner, RetrieveRemoveOrder, UpdateOrder 


router = DefaultRouter()

router.register('categories', CategoryViewSet, basename='categories')
router.register('order_items', OrderItemViewSet, basename='order_items')

urlpatterns = [
    # User urls
    path('users/', ListUsers.as_view(), name="list_users"),
    path('users/<int:pk>/', RetrieveUser.as_view(), name="user_detail"),
    path('users/<int:pk>/update/', UpdateUser.as_view(), name="user_update__view"),
    path('users/<int:pk>/remove/', RemoveUser.as_view(), name="user_destroy_view"),
    path('users/auth/register/', UserCreateView.as_view(), name="create_a_user"),
    path('users/auth/login/', UserLoginView.as_view(), name="user_login"),
    path('users/auth/logout/', UserLogoutView.as_view(), name="user_logout"),

    # Product urls
    path('products/add/', CreateProduct.as_view(), name="add_products"),
    path('products/', ListProducts.as_view(), name="list_products"),
    path('products/<int:pk>/', RetrieveProduct.as_view(), name="product_detail_view"),
    path('products/<int:pk>/update/', UpdateProduct.as_view(), name="update_product"),
    path('products/<int:pk>/remove/', RemoveProduct.as_view(), name="remove_product"),

    # Cart urls
    # path('carts/add/', CreateCart.as_view(), name="add_carts"),
    path('carts/', ListCarts.as_view(), name="list_carts"),
    path('carts/<int:pk>/', RetrieveRemoveCart.as_view(), name="cart_retrieve_destroy"),
    # path('carts/<int:pk>/remove/', RemoveCart.as_view(), name="cart_remove"),

    # CartItem urls
    path('carts/add_items/', CreateCartItem.as_view(), name="add_carts_items"),
    path('carts/items/', ListCartItems.as_view(), name="list_cartitems"),
    path('carts/<int:pk>/items/', AdminListCartItems.as_view(), name="admin_list_cartitems"),
    path('carts/<int:cart_pk>/items/<int:pk>/update/', UpdateCartItem.as_view(), name="cart_upadte"),
    path('carts/<int:cart_pk>/items/<int:pk>/remove/', RemoveCartItem.as_view(), name="remove_cart"),

    # Order urls
    path('orders/all_orders/', AdminListOrders.as_view(), name="list orders"),
    path('orders/', ListOrdersByOwner.as_view(), name="list orders"),
    path('orders/create/', CreateOrder.as_view(), name="creat_order"),
    path('orders/<int:pk>/', RetrieveRemoveOrder.as_view(), name="retrieve_order"),
    path('orders/<int:pk>/update/', UpdateOrder.as_view(), name="order_upadte"),
    # path('carts/<int:cart_pk>/items/<int:pk>/remove/', RemoveCartItem.as_view(), name="remove_cart"),
] 

urlpatterns += router.urls