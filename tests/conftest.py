import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from tests.test_users.factories import UserProfileFactory


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def authenticated_admin_client():
    client = APIClient()
    user_profile = UserProfileFactory(role="admin")
    token = Token.objects.create(user=user_profile.user)
    client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
    return client


@pytest.fixture
def authenticated_buyer_client():
    client = APIClient()
    user_profile = UserProfileFactory()
    token = Token.objects.create(user=user_profile.user)
    client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
    return client
