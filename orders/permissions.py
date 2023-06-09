from rest_framework import permissions


class OrderPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.profile.role == "admin":
            return True
        if view.action == "create" or view.action == "retrieve":
            return request.user.is_authenticated and request.user.profile.role == "buyer"
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user.profile.role == "admin":
            return True
        if view.action == "retrieve":
            return obj.customer == request.user
        return True


class OrderItemPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == "create":
            return False
        if request.user.is_authenticated and request.user.profile.role == "admin":
            return True
        if view.action == "retrieve":
            return request.user.is_authenticated and request.user.profile.role == "buyer"
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user.profile.role == "admin":
            return True
        if view.action == "retrieve":
            return obj.order.customer == request.user
        return True
