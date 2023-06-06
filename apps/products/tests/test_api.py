from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.products.models import Product
from apps.users.models import CustomUser
from rest_framework_simplejwt.tokens import AccessToken


class ProductTests(TestCase):
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

    def test_create_product_unauthorized(self):
        url = reverse('product-list')
        data = {'name': 'Novo Produto', 'price': 50, 'category_id': 1}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_product_unauthorized(self):
        product_id = 1  # ID do produto na fixture
        url = reverse('product-detail', args=[product_id])
        data = {'name': 'Produto Atualizado', 'price': 15, 'category_id': 2}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_product_unauthorized(self):
        product_id = 1  # ID do produto na fixture
        url = reverse('product-detail', args=[product_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_product_authorized(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_seller}')
        url = reverse('product-list')
        data = {'name': 'Novo Produto', 'price': 50, 'category_id': 1}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_product_authorized(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_seller}')
        product_id = 1  # ID do produto na fixture
        url = reverse('product-detail', args=[product_id])
        data = {'name': 'Produto Atualizado', 'price': 15, 'category_id': 2}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_product_authorized(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_seller}')
        product_id = 1  # ID do produto na fixture
        url = reverse('product-detail', args=[product_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(pk=product_id).exists())
