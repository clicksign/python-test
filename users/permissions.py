from rest_framework import permissions


class UserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.profile.role == "admin":
            return True
        if view.action == "create" and not request.user.is_authenticated:
            return True
        if view.action == "retrieve" and request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user.profile.role == "admin":
            return True
        if view.action == "retrieve":
            return obj.username == request.user
        return False


class UserProfilePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.profile.role == "admin":
            return True
        if view.action == "create" and not request.user.is_authenticated:
            return True
        if view.action == "retrieve" and request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user.profile.role == "admin":
            return True
        if view.action == "retrieve":
            return obj.user.username == request.user
        return False
