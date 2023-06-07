from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken
from apps.products.models import Product, Category
from apps.users.models import CustomUser


class OrderTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username='clienteteste', password='senha123', user_group=2)
        self.other_user = CustomUser.objects.create_user(
            username='outroclienteteste', password='senha456', user_group=2)
        self.token = AccessToken.for_user(self.user)
        self.other_token = AccessToken.for_user(self.other_user)

        self.category_material = Category.objects.create(id=1, name='Material Escolar')
        self.category_construction = Category.objects.create(id=4, name='Construção')

    def create_product(self, name, price, category):
        return Product.objects.create(name=name, price=price, category=category)

    def create_order(self, order_items, token):
        url = reverse('order-list')
        data = {'order_items': order_items}
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = client.post(url, data, format='json')
        return response.status_code, response.data

    def test_create_order(self):
        product_material = self.create_product(
            name='Produto Material', price=100, category=self.category_material
        )

        order_items = [{'product_id': product_material.id, 'quantity': 3}]
        status_code, response_data = self.create_order(order_items, self.token)

        self.assertEqual(status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response_data['order_items']), 1)
        self.assertEqual(response_data['order_items'][0]['product']['id'], product_material.id)
        self.assertEqual(response_data['order_items'][0]['quantity'], 3)

    def test_update_order(self):
        product_material = self.create_product(
            name='Produto Material', price=100, category=self.category_material
        )
        product_construction = self.create_product(
            name='Produto Construção', price=200, category=self.category_construction
        )

        order_items = [{'product_id': product_material.id, 'quantity': 3}]
        status_code, response_data = self.create_order(order_items, self.token)
        order_id = response_data['id']

        url = reverse('order-detail', args=[order_id])
        data = {'order_items': [{'product_id': product_construction.id, 'quantity': 5}]}
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = client.patch(url, data, format='json')
        products_ids = [item['product']['id'] for item in response.data['order_items']]
        quantities = [item['quantity'] for item in response.data['order_items']]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(product_material.id, products_ids)
        self.assertEqual(quantities, [3, 5])

    def test_update_other_order(self):
        product_material = self.create_product(
            name='Produto Material', price=100, category=self.category_material
        )
        product_construction = self.create_product(
            name='Produto Construção', price=200, category=self.category_construction
        )

        own_order_items = [{'product_id': product_material.id, 'quantity': 3}]
        own_order_id = self.create_order(own_order_items, self.token)[1]['id']

        other_order_items = [{'product_id': product_construction.id, 'quantity': 5}]
        other_order_id = self.create_order(other_order_items, self.other_token)[1]['id']

        url = reverse('order-detail', args=[other_order_id])
        data = {'order_items': [{'product_id': product_material.id, 'quantity': 3}]}
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        url = reverse('order-detail', args=[own_order_id])
        data = {'order_items': [{'product_id': product_construction.id, 'quantity': 5}]}
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.other_token}')
        response = client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_order(self):
        product_material = self.create_product(
            name='Produto Material', price=100, category=self.category_material
        )

        order_items = [{'product_id': product_material.id, 'quantity': 3}]
        status_code, response_data = self.create_order(order_items, self.token)
        order_id = response_data['id']

        url = reverse('order-detail', args=[order_id])
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_other_order(self):
        product_material = self.create_product(
            name='Produto Material', price=100, category=self.category_material
        )
        product_construction = self.create_product(
            name='Produto Construção', price=200, category=self.category_construction
        )

        own_order_items = [{'product_id': product_material.id, 'quantity': 3}]
        self.create_order(own_order_items, self.token)[1]['id']

        other_order_items = [{'product_id': product_construction.id, 'quantity': 5}]
        other_order_id = self.create_order(other_order_items, self.other_token)[1]['id']

        url = reverse('order-detail', args=[other_order_id])
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_discounts(self):
        product_material = self.create_product(
            name='Produto Material', price=100, category=self.category_material
        )
        product_construction = self.create_product(
            name='Produto Construção', price=200, category=self.category_construction
        )

        # 1. 15% discount for orders with 2 or more items from the category "Material Escolar"
        # total = (100 * 3) - (100 * 3 * 0.15) = 255
        order_items = [{'product_id': product_material.id, 'quantity': 3}]
        status_code, response_data = self.create_order(order_items, self.token)
        order_id = response_data['id']

        url = reverse('order-detail', args=[order_id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total'], '255.00')

        # 2. 5% discount for orders with 3 or more items from the category "Material de construção"
        # total = (200 * 3) - (200 * 3 * 0.05) = 570
        order_items = [{'product_id': product_construction.id, 'quantity': 3}]
        status_code, response_data = self.create_order(order_items, self.token)
        order_id = response_data['id']

        url = reverse('order-detail', args=[order_id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total'], '570.00')

        # 3. 7% discount for orders with 5 or more items from the category "Material de construção"
        # total = (200 * 5) - (200 * 5 * 0.07) = 930
        order_items = [{'product_id': product_construction.id, 'quantity': 5}]
        status_code, response_data = self.create_order(order_items, self.token)
        order_id = response_data['id']

        url = reverse('order-detail', args=[order_id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total'], '930.00')
