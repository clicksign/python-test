from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from apps.users.permissions import IsOwnerOrReadOnly, CLIENT_GROUP_ID
from apps.orders.models import Order
from apps.orders.serializers import OrderSerializer
from apps.orders.filters import OrderFilter


@extend_schema(tags=['Orders'])
class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)
    filterset_class = OrderFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.user_group == CLIENT_GROUP_ID:
            queryset = queryset.filter(user=self.request.user)
        return queryset


@extend_schema(tags=['Orders'])
class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)
