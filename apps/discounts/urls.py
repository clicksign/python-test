from django.urls import path
from apps.discounts import views


urlpatterns = [
    path('', views.DiscountList.as_view(), name='discount-list'),
    path('<int:pk>/', views.DiscountDetail.as_view(), name='discount-detail'),
]
