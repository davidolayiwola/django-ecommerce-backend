# Built in classes
from rest_framework.test import APITestCase

from rest_framework.authtoken.models import Token
from rest_framework import status

# from django.urls import reverse

# Model classes
from .models import CustomUser, ProductModel, CategoryModel, CartModel
from .models import CartItemModel, OrderModel, OrderItemModel

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



"""
    Product View Test Methods/Cases
"""
class ProductAPITest(APITestCase):
    """Tests for ProductAPITest using APIRequestFactory."""

    def setUp(self):
        """Prepare the test environment before each test"""

        # Create user and token
        self.user1 = CustomUser.objects.create_user(email="admin_user_1@gmail.com", password="testuser123", is_staff=True)
        self.user2 = CustomUser.objects.create_user(email="user_1@gmail.com", password="testuser123")

        self.admin_token, admin_created = Token.objects.get_or_create(user=self.user1)
        self.user_token, user_created = Token.objects.get_or_create(user=self.user2)

        self.client.credentials()

        # Create test data for Category
        self.category = CategoryModel.objects.create(name="Electronics")

        # Create test data for Product
        self.product = ProductModel.objects.create(
            name = "PS 3",
            description = "A Better Gaming Device",
            brand = "Sony",
            price = 48.00,
            quantity = 7,
            category = self.category,
            release_date = "2026-09-04"
        )

    def tearDown(self):
        """Clean up test data after each test"""

        self.user1.delete()
        self.user2.delete()
        self.category.delete()
        self.product.delete()

    def test_list_products(self):
        """Test the list products endpoint."""

        response = self.client.get("/api/v1/products/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), ProductModel.objects.count())

    def test_detail_product(self):
        """Test the product detail endpoint."""
        
        response = self.client.get("/api/v1/products/", args=(self.product.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(ProductModel.objects.filter(pk=self.product.id).exists())

    def test_create_product_with_authenticated_admin(self):
        """Test creating a new product endpoint with authenticated admin."""

        data = {
            "name": "PS 2",
            "description": "A Gaming Device",
            "brand": "Sony",
            "price": 45.00,
            "quantity": 3,
            "category": 1,
            "release_date": "2026-06-14"
        }

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.admin_token.key}")
        response = self.client.post("/api/v1/products/add/", data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], data["name"])

    def test_create_product_with_authenticated_user(self):
        """Test creating a new product endpoint with authenticated user."""

        data = {
            "name": "PS 2",
            "description": "A Gaming Device",
            "brand": "Sony",
            "price": 45.00,
            "quantity": 3,
            "category": 1,
            "release_date": "2026-06-14"
        }

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.user_token.key}")
        response = self.client.post("/api/v1/products/add/", data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {"detail": "You do not have permission to perform this action."})

    def test_create_product_with_unauthenticated_user(self):
        """Test the create product endpoint with unauthenticated user."""
        data = {
            "name": "PS 2",
            "description": "A Gaming Device",
            "brand": "Sony",
            "price": 45.00,
            "quantity": 3,
            "category": 1,
            "release_date": "2026-06-14"
        }

        self.client.credentials()
        response = self.client.post("/api/v1/products/add/", data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {"detail": "Authentication credentials were not provided."})


    def test_update_product_with_authenticated_admin(self):
        """Test the update product endpoint with authenticated admin."""

        # Testing data
        data = {
            "description": "A Smart Gaming Device",
        }

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.admin_token.key}")
        response = self.client.patch(f"/api/v1/products/{self.product.id}/update/", data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.description, data["description"])

    def test_update_product_with_authenticated_user(self):
        """Test the update product endpoint with authenticated user."""

        # Testing data
        data = {
            "description": "A Smart Gaming Device",
        }

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.user_token.key}")
        response = self.client.patch(f"/api/v1/products/{self.product.id}/update/", data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # self.product.refresh_from_db()
        self.assertEqual(response.data, {"detail": "You do not have permission to perform this action."})

    def test_update_product_with_unauthenticated_user(self):
        """Test the update product endpoint with unauthenticated user."""

        # Testing data
        data = {
            "description": "A Smart Gaming Device",
        }

        self.client.credentials()
        response = self.client.patch(f"/api/v1/products/{self.product.id}/update/", data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # self.product.refresh_from_db()
        self.assertEqual(response.data, {"detail": "Authentication credentials were not provided."})

    def test_remove_product_with_authenticated_admin(self):
        """Test the remove product endpoint with authenticated admin."""

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.admin_token.key}")
        response = self.client.delete(f"/api/v1/products/{self.product.id}/remove/", args=(self.product.id))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ProductModel.objects.filter(id=self.product.id).exists())

    def test_remove_product_with_authenticated_user(self):
        """Test the remove product endpoint with authenticated user."""

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.user_token.key}")
        response = self.client.delete(f"/api/v1/products/{self.product.id}/remove/", args=(self.product.id))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {"detail": "You do not have permission to perform this action."})

    def test_remove_product_with_unauthenticated_user(self):
        """Test the remove product endpoint with unauthenticated user."""

        self.client.credentials()
        response = self.client.delete(f"/api/v1/products/{self.product.id}/remove/", args=(self.product.id))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {"detail": "Authentication credentials were not provided."})


"""
    Cart View Test Methods/Cases
"""
class CartAPITest(APITestCase):
    """Tests for ProductAPITest using APIRequestFactory."""

    def setUp(self):
        """Prepare the test environment before each test"""

        # Create user and token
        self.user1 = CustomUser.objects.create_user(email="admin_user_1@gmail.com", password="testuser123", is_staff=True)
        self.user2 = CustomUser.objects.create_user(email="user_1@gmail.com", password="testuser123")

        self.admin_token, admin_created = Token.objects.get_or_create(user=self.user1)
        self.user_token, user_created = Token.objects.get_or_create(user=self.user2)

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.admin_token.key}")

        self.cart = CartModel.objects.create(user=self.user2)

    def tearDown(self):
        """Clean up test data after each test"""

        self.user1.delete()
        self.user2.delete()
        self.cart.delete()

    def test_list_carts_with_authenticated_admin(self):
        """Test the list carts endpoint with authenticated admin."""

        response = self.client.get("/api/v1/carts/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), CartModel.objects.count())

    def test_list_carts_with_authenticated_user(self):
        """Test the list carts endpoint with authenticated user."""

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.user_token.key}")
        response = self.client.get("/api/v1/carts/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {"detail": "You do not have permission to perform this action."})

    def test_list_carts_with_unauthenticated_user(self):
        """Test the list carts endpoint with unauthenticated user."""

        self.client.credentials()
        response = self.client.get("/api/v1/carts/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {"detail": "Authentication credentials were not provided."})

    def test_detail_cart_with_authenticated_admin(self):
        """Test the product deatail endpoint with authenticated admin."""

        response = self.client.get("/api/v1/carts/", args=(self.cart.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(CartModel.objects.filter(pk=self.cart.id).exists())

    def test_detail_cart_with_authenticated_user(self):
        """Test the product deatail endpoint with authenticated user."""

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.user_token.key}")
        response = self.client.get("/api/v1/carts/", args=(self.cart.id))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {"detail": "You do not have permission to perform this action."})

    def test_detail_cart_with_unauthenticated_user(self):
        """Test the product deatail endpoint with unauthenticated user."""

        self.client.credentials()
        response = self.client.get("/api/v1/carts/", args=(self.cart.id))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {"detail": "Authentication credentials were not provided."})

    def test_remove_cart_with_authenticated_admin(self):
        """Test the remove cart endpoint with authenticated admin."""

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.admin_token.key}")
        response = self.client.delete(f"/api/v1/carts/{self.cart.id}/")
        # response = self.client.delete("/api/v1/carts/", args=(self.cart.id))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CartModel.objects.filter(id=self.cart.id).exists())

    def test_remove_cart_with_authenticated_user(self):
        """Test the remove cart endpoint with authenticated user."""

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.user_token.key}")
        response = self.client.delete("/api/v1/carts/", args=(self.cart.id))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {"detail": "You do not have permission to perform this action."})

    def test_remove_cart_with_unauthenticated_user(self):
        """Test the remove product endpoint with unauthenticated user."""

        self.client.credentials()
        response = self.client.delete("/api/v1/carts/", args=(self.cart.id))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {"detail": "Authentication credentials were not provided."})


"""
    Order View Test Methods/Cases
"""
class OrderAPITest(APITestCase):
    """Tests for OrderAPITest using APIRequestFactory."""

    def setUp(self):
        """Prepare the test environment before each test"""

        # Create test user and token for authentication
        # self.factory = APIRequestFactory(enforce_csrf_checks=True)
        self.user1 = CustomUser.objects.create_user(email="admin_user_1@gmail.com", password="testuser123", is_staff=True)
        self.user2 = CustomUser.objects.create_user(email="user_1@gmail.com", password="testuser123")
        self.user3 = CustomUser.objects.create_user(email="user_2@gmail.com", password="testuser123")

        self.admin_token, admin_created = Token.objects.get_or_create(user=self.user1)
        self.ordinary_user_token, user1_created = Token.objects.get_or_create(user=self.user2)
        self.user_owner_token, user2_created = Token.objects.get_or_create(user=self.user3)

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.admin_token.key}")

        # print(f"Client is {self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.admin_token.key}")}")

        # Create test data for order
        self.order = OrderModel.objects.create(
            user = self.user3,
            total_price = 90.6,
            status = "pending",
            shipping_address = "Mokola street"
        )

    def tearDown(self):
        """Clean up test data after each test"""

        self.order.delete()
        self.user1.delete()
        self.user2.delete()
        self.user3.delete()

    def test_list_orders_with_authenticated_admin(self):
        """Test the list orders endpoint with authenticated admin."""

        # reverse arguments are reverse(basename-list)
        response = self.client.get("/api/v1/orders/all_orders/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(len(response.data["results"]), OrderModel.objects.count())

    def test_list_orders_with_authenticated_owner(self):
        """Test the list orders endpoint with authenticated user."""

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.user_owner_token.key}")
        response = self.client.get("/api/v1/orders/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(len(response.data["results"]), OrderModel.objects.count())

    def test_list_orders_with_authenticated_user_but_not_owner(self):
        """Test the list orders endpoint with unauthenticated user."""

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.ordinary_user_token.key}")
        response = self.client.get("/api/v1/orders/")

        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)


    def test_list_orders_with_unauthenticated_user(self):
        """Test the list orders endpoint with unauthenticated user."""

        self.client.credentials()
        response = self.client.get("/api/v1/orders/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {"detail": "Authentication credentials were not provided."})

    def test_detail_order_with_authenticated_admin(self):
        """Test the order deatail endpoint with authenticated admin."""
        
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.admin_token.key}")
        response = self.client.get(f"/api/v1/orders/", args=(self.order.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(OrderModel.objects.filter(pk=self.order.id).exists())

    def test_detail_order_with_authenticated_user_and_order_owner(self):
        """Test the order deatail endpoint with authenticated user."""
        
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.user_owner_token.key}")
        response = self.client.get(f"/api/v1/orders/", args=(self.order.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(OrderModel.objects.filter(pk=self.order.id).exists())

    def test_detail_order_with_authenticated_user_but_not_order_owner(self):
        """Test the order deatail endpoint with authenticated user but not owner yet to be fixed."""
        
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.ordinary_user_token.key}")
        response = self.client.get(f"/api/v1/orders/{self.order.id}/", args=(self.order.id))

        print(f"Detail is {response.data}")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {"detail": "You do not have permission to perform this action."})

    def test_detail_order_with_unauthenticated_user(self):
        """Test the order deatail endpoint with unauthenticated user."""

        self.client.credentials()
        response = self.client.get(f"/api/v1/orders/", args=(self.order.id))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {"detail": "Authentication credentials were not provided."})

    def test_create_order_with_authenticated_user(self):
        """Test creating a new order endpoint with authenticated user. """

        data = {
            "user": self.user2.id,
            "total_price": 90.6,
            "status": "pending",
            "shipping_address": "Mokola street"
        }

        # Create client and make post request
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.ordinary_user_token.key}")
        response = self.client.post("/api/v1/orders/create/", data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["shipping_address"], data["shipping_address"])

    def test_create_order_with_unauthenticated_user(self):
        """Test the create order endpoint with unauthenticated user."""

        data = {
            "user" : self.user2,
            "total_price" : 90.6,
            "status" : "pending",
            "shipping_address" : "Mokola street"
        }

        # Create client and make post request
        self.client.credentials()
        response = self.client.post("/api/v1/orders/create/", data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {"detail": "Authentication credentials were not provided."})


    def test_update_order_with_authenticated_user_and_order_owner(self):
        """Test the order deatail endpoint with authenticated user."""

        data = {
            "shipping_address": "Adekola Street"
        }

        # Create client and make post request
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.user_owner_token.key}")
        response = self.client.patch(f"/api/v1/orders/{self.order.id}/update/", data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.shipping_address, data["shipping_address"])

    def test_update_order_with_authenticated_user_but_not_order_owner(self):
        """Test the order deatail endpoint with authenticated user."""
        data = {
            "shipping_address": "Adekola Street"
        }

        # Create client and make post request
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.ordinary_user_token.key}")
        response = self.client.patch(f"/api/v1/orders/{self.order.id}/update/", data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {"detail": "You do not have permission to perform this action."})

    def test_update_order_with_unauthenticated_user(self):
        """Test the order deatail endpoint with unauthenticated user."""
        data = {
            "shipping_address": "Adekola Street"
        }

        # Create client and make post request
        self.client.credentials()
        response = self.client.patch(f"/api/v1/orders/{self.order.id}/update/", data)

        # print(f"Data response is {response.data}")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {"detail": "Authentication credentials were not provided."})

    def test_remove_order_with_authenticated_admin(self):
        """Test the order remove endpoint with authenticated admin."""

        # Create client and make post request
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.admin_token.key}")
        response = self.client.delete(f"/api/v1/orders/{self.order.id}/")
    
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(OrderModel.objects.filter(pk=self.order.id).exists())

    def test_remove_order_with_authenticated_user_and_order_owner(self):
        """Test the order remove endpoint with authenticated user and owner."""

        # Create client and make post request
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.user_owner_token.key}")
        response = self.client.delete(f"/api/v1/orders/{self.order.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(OrderModel.objects.filter(pk=self.order.id).exists())

    def test_remove_order_with_authenticated_user_but_not_order_owner(self):
        """Test the order remove endpoint with authenticated user but not an owner."""

        # Create client and make post request
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.ordinary_user_token.key}")
        response = self.client.delete(f"/api/v1/orders/{self.order.id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {"detail": "You do not have permission to perform this action."})

    def test_remove_order_with_unauthenticated_user(self):
        """Test the order remove endpoint with unauthenticated user."""

        # Create client and make post request
        self.client.credentials()
        response = self.client.delete(f"/api/v1/orders/{self.order.id}/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {"detail": "Authentication credentials were not provided."})
