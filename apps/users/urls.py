from django.urls import path
from apps.users import views


urlpatterns = [
    path('', views.UserListCreateView.as_view(), name='users'),
    path('<int:pk>/', views.UserRetrieveUpdateDestroyView.as_view(), name='user'),
]
