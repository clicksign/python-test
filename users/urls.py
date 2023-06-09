from django.urls import include, path
from rest_framework import routers

from .views import UserProfileViewSet, UserViewSet

router = routers.DefaultRouter()
router.register("users", UserViewSet)
router.register("profiles", UserProfileViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
