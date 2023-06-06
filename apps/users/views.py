from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from apps.users.serializers import CustomUserSerializer
from apps.users.models import CustomUser


@extend_schema(tags=['Users'])
class UserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)


@extend_schema(tags=['Users'])
class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)
