from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.models import CustomUser


class UserSetupMixin:
    def setUp(self):
        self.client = APIClient()
        self.admin_user = CustomUser.objects.create_superuser(
            username='admin', password='adminpassword')
        self.client_user = CustomUser.objects.create_user(
            username='client', password='clientpassword', user_group=2)
        self.seller_user = CustomUser.objects.create_user(
            username='seller', password='sellerpassword', user_group=3)
        self.admin_token = self.generate_access_token(self.admin_user)
        self.client_token = self.generate_access_token(self.client_user)
        self.seller_token = self.generate_access_token(self.seller_user)

    @staticmethod
    def generate_access_token(user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class UserTests(UserSetupMixin, TestCase):
    def test_list_users_unauthorized(self):
        url = reverse('users')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_user(self):
        user_id = self.admin_user.id
        url = reverse('user', args=[user_id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'admin')

    def test_update_user(self):
        user_id = self.admin_user.id
        url = reverse('user', args=[user_id])
        data = {'username': 'newusername'}
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'newusername')

    def test_delete_user_unauthorized(self):
        user_id = self.client_user.id
        url = reverse('user', args=[user_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_user_authorized_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        user_id = self.client_user.id
        url = reverse('user', args=[user_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CustomUser.objects.filter(pk=user_id).exists())


class UserAuthorizationTests(UserSetupMixin, TestCase):
    def test_list_users_authorized(self):
        authorization_tests = [
            {'user': self.admin_user, 'status_code': status.HTTP_200_OK},
            {'user': self.client_user, 'status_code': status.HTTP_403_FORBIDDEN},
            {'user': self.seller_user, 'status_code': status.HTTP_403_FORBIDDEN},
        ]

        for test in authorization_tests:
            self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.generate_access_token(test["user"])}')
            url = reverse('users')
            response = self.client.get(url)
            self.assertEqual(response.status_code, test['status_code'])

    def test_create_user_unauthorized(self):
        url = reverse('users')
        data = {'username': 'newuser', 'password': 'newpassword', 'user_group': 2}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_user_authorized_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('users')
        data = {'username': 'newuser', 'password': 'newpassword', 'user_group': 2}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_authorized(self):
        authorization_tests = [
            {'user': self.client_user, 'status_code': status.HTTP_403_FORBIDDEN},
            {'user': self.seller_user, 'status_code': status.HTTP_403_FORBIDDEN},
        ]

        for test in authorization_tests:
            self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.generate_access_token(test["user"])}')
            url = reverse('users')
            data = {'username': 'newuser', 'password': 'newpassword', 'user_group': 2}
            response = self.client.post(url, data)
            self.assertEqual(response.status_code, test['status_code'])

    def test_update_user_unauthorized(self):
        user_id = self.admin_user.id
        url = reverse('user', args=[user_id])
        data = {'username': 'newusername'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user_authorized_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        user_id = self.admin_user.id
        url = reverse('user', args=[user_id])
        data = {'username': 'newusername'}
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'newusername')

    def test_update_user_authorized(self):
        authorization_tests = [
            {'user': self.client_user, 'status_code': status.HTTP_403_FORBIDDEN},
            {'user': self.seller_user, 'status_code': status.HTTP_403_FORBIDDEN},
        ]

        for test in authorization_tests:
            self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.generate_access_token(test["user"])}')
            user_id = self.admin_user.id
            url = reverse('user', args=[user_id])
            data = {'username': 'newusername'}
            response = self.client.put(url, data)
            self.assertEqual(response.status_code, test['status_code'])

    def test_delete_user_authorized(self):
        authorization_tests = [
            {'user': self.admin_user, 'status_code': status.HTTP_204_NO_CONTENT},
            {'user': self.client_user, 'status_code': status.HTTP_403_FORBIDDEN},
            {'user': self.seller_user, 'status_code': status.HTTP_403_FORBIDDEN},
        ]

        for test in authorization_tests:
            self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.generate_access_token(test["user"])}')
            user_id = self.admin_user.id
            url = reverse('user', args=[user_id])
            response = self.client.delete(url)
            self.assertEqual(response.status_code, test['status_code'])
            if test['status_code'] == status.HTTP_204_NO_CONTENT:
                self.assertFalse(CustomUser.objects.filter(pk=user_id).exists())
