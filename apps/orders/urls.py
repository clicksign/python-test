from django.urls import path
from apps.orders import views


urlpatterns = [
    path('', views.OrderList.as_view(), name='order-list'),
    path('<int:pk>/', views.OrderDetail.as_view(), name='order-detail'),
]
