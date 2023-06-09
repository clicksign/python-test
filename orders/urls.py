from django.urls import include, path
from rest_framework import routers

from .views import OrderItemViewSet, OrderViewSet

router = routers.DefaultRouter()
router.register("orders", OrderViewSet)
router.register("order-items", OrderItemViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
