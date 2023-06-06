from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.categories.models import Category
from apps.users.models import CustomUser
from rest_framework_simplejwt.tokens import AccessToken


class CategoryTests(TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.client = APIClient()
        self.user_client = CustomUser.objects.create_user(
            username='clienteteste', password='senha123', user_group=2)
        self.user_seller = CustomUser.objects.create_user(
            username='vendedorteste', password='senha123', user_group=3)
        self.token_client = AccessToken.for_user(self.user_client)
        self.token_seller = AccessToken.for_user(self.user_seller)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_client}')

    def test_create_category_unauthorized(self):
        url = reverse('category-list')
        data = {'name': 'Nova Categoria'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_category_unauthorized(self):
        category_id = 1  # ID da categoria na fixture
        url = reverse('category-detail', args=[category_id])
        data = {'name': 'Categoria Atualizada'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_category_unauthorized(self):
        category_id = 1  # ID da categoria na fixture
        url = reverse('category-detail', args=[category_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_category_authorized(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_seller}')
        url = reverse('category-list')
        data = {'name': 'Nova Categoria'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_category_authorized(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_seller}')
        category_id = 1  # ID da categoria na fixture
        url = reverse('category-detail', args=[category_id])
        data = {'name': 'Categoria Atualizada'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_category_authorized(self):
        category = Category.objects.create(name="Test Category")
        category_id = category.id
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_seller}')
        url = reverse('category-detail', args=[category_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(pk=category_id).exists())
