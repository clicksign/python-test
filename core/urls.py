from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    # Drf Spectacular
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/docs/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Apps
    path('api/users/', include('apps.users.urls')),

    # Django Admin
    path('admin/', admin.site.urls),
]
