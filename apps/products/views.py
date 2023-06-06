from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from apps.products.models import Product
from apps.users.permissions import IsSellerAdminOrReadOnly
from apps.products.serializers import ProductSerializer
from apps.products.filters import ProductFilter


@extend_schema(tags=['Products'])
class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated, IsSellerAdminOrReadOnly,)
    filterset_class = ProductFilter


@extend_schema(tags=['Products'])
class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated, IsSellerAdminOrReadOnly,)
