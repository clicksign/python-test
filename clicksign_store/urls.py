from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.authtoken import views as authtoken_views

schema_view = get_schema_view(
    openapi.Info(
        title="ClickSign Store API",
        default_version="v1",
        description="API documentation for ClickSign Store",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("", RedirectView.as_view(url="v1/docs/", permanent=False)),
    path("v1/login/", authtoken_views.obtain_auth_token),
    path("v1/admin/", admin.site.urls),
    path("v1/", include("products.urls")),
    path("v1/", include("orders.urls")),
    path("v1/", include("users.urls")),
    path("v1/docs/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]
