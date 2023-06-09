from django.urls import include, path
from rest_framework import routers

from .views import CategoryDiscountViewSet, CategoryViewSet, ProductViewSet

router = routers.DefaultRouter()
router.register("categories", CategoryViewSet)
router.register("category-discounts", CategoryDiscountViewSet)
router.register("products", ProductViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
