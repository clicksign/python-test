from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from apps.users.permissions import IsAdminOrSeller
from apps.discounts.models import Discount
from apps.discounts.serializers import DiscountSerializer


@extend_schema(tags=['Discounts'])
class DiscountList(generics.ListCreateAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = (IsAuthenticated, IsAdminOrSeller,)


@extend_schema(tags=['Discounts'])
class DiscountDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = (IsAuthenticated, IsAdminOrSeller,)
