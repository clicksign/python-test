from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from apps.users.permissions import IsSellerAdminOrReadOnly
from apps.categories.models import Category
from apps.categories.serializers import CategorySerializer


@extend_schema(tags=['Categories'])
class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated, IsSellerAdminOrReadOnly,)


@extend_schema(tags=['Categories'])
class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated, IsSellerAdminOrReadOnly,)
