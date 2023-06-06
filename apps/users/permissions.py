from rest_framework import permissions
from apps.users.models import CustomUser

USER_GROUPS = CustomUser.USER_GROUPS
ADMIN_GROUP_ID = [group[0] for group in USER_GROUPS if group[1] == 'Admin'][0]
SELLER_GROUP_ID = [group[0] for group in USER_GROUPS if group[1] == 'Seller'][0]
CLIENT_GROUP_ID = [group[0] for group in USER_GROUPS if group[1] == 'Client'][0]


class IsSellerAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow sellers and admins to edit it.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.user_group in [ADMIN_GROUP_ID, SELLER_GROUP_ID]
