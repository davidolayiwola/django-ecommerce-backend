from rest_framework.permissions import BasePermission

from .models import CustomUser, CartModel, OrderModel

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsOwnerOrAdminUser(BasePermission):
    # print(f"E reach here first")
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, CustomUser):
            # print(f"E reach here second")
            return obj == request.user or request.user.is_staff
            # return obj.owner == request.user
        else:
            # print(f"E reach here oooo")
            return obj.user == request.user or request.user.is_staff
            # return obj.owner == request.user


class IsCartOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = CustomUser.objects.get(pk=CartModel.objects.get(pk=obj.cart.id).id)
        return user == request.user