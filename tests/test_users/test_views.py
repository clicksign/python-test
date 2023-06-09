import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

from .factories import UserFactory, UserProfileFactory
from users.models import UserProfile

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "client_fixture, expected_status, expected_length",
    [
        ("authenticated_admin_client", status.HTTP_200_OK, 6),
        ("authenticated_buyer_client", status.HTTP_403_FORBIDDEN, 1),
        ("client", status.HTTP_401_UNAUTHORIZED, 1),
    ],
)
def test_list_users(client_fixture, expected_status, expected_length, request):
    client = request.getfixturevalue(client_fixture)
    UserProfileFactory.create_batch(5)
    url = reverse("user-list")
    response = client.get(url)
    assert response.status_code == expected_status
    assert len(response.data) == expected_length


@pytest.mark.parametrize(
    "client_fixture, expected_status",
    [
        ("authenticated_admin_client", status.HTTP_200_OK),
        ("authenticated_buyer_client", status.HTTP_403_FORBIDDEN),
        ("client", status.HTTP_401_UNAUTHORIZED),
    ],
)
def test_retrieve_user(client_fixture, expected_status, request):
    client = request.getfixturevalue(client_fixture)
    user = UserProfileFactory()
    url = reverse("user-detail", args=[user.id])
    response = client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "client_fixture, expected_status, expected_create",
    [
        ("authenticated_admin_client", status.HTTP_201_CREATED, True),
        ("authenticated_buyer_client", status.HTTP_403_FORBIDDEN, False),
        ("client", status.HTTP_201_CREATED, True),
    ],
)
def test_create_user(client_fixture, expected_status, expected_create, request):
    client = request.getfixturevalue(client_fixture)
    url = reverse("user-list")
    data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword",
        "profile": {
            "name": "Test User",
            "role": "buyer",
            "phone_number": "1234567890",
            "address": "Test Address",
        },
    }
    response = client.post(url, data, format="json")
    assert response.status_code == expected_status
    assert User.objects.filter(username="testuser").exists() is expected_create


@pytest.mark.parametrize(
    "client_fixture, expected_status",
    [
        ("authenticated_admin_client", status.HTTP_200_OK),
        ("authenticated_buyer_client", status.HTTP_403_FORBIDDEN),
        ("client", status.HTTP_401_UNAUTHORIZED),
    ],
)
def test_update_user(client_fixture, expected_status, request):
    client = request.getfixturevalue(client_fixture)
    user = UserFactory()
    url = reverse("user-detail", args=[user.id])
    data = {"username": "updateduser"}
    response = client.patch(url, data, format="json")
    assert response.status_code == expected_status
    if expected_status == status.HTTP_200_OK:
        user.refresh_from_db()
        assert user.username == "updateduser"


@pytest.mark.parametrize(
    "client_fixture, expected_status",
    [
        ("authenticated_admin_client", status.HTTP_204_NO_CONTENT),
        ("authenticated_buyer_client", status.HTTP_403_FORBIDDEN),
        ("client", status.HTTP_401_UNAUTHORIZED),
    ],
)
def test_delete_user(client_fixture, expected_status, request):
    client = request.getfixturevalue(client_fixture)
    user = UserFactory()
    url = reverse("user-detail", args=[user.id])
    response = client.delete(url)
    assert response.status_code == expected_status
    if expected_status == status.HTTP_204_NO_CONTENT:
        assert not User.objects.filter(id=user.id).exists()


@pytest.mark.parametrize(
    "client_fixture, expected_status, expected_length",
    [
        ("authenticated_admin_client", status.HTTP_200_OK, 6),
        ("authenticated_buyer_client", status.HTTP_403_FORBIDDEN, 1),
        ("client", status.HTTP_401_UNAUTHORIZED, 1),
    ],
)
def test_list_user_profiles(client_fixture, expected_status, expected_length, request):
    client = request.getfixturevalue(client_fixture)
    UserProfileFactory.create_batch(5)
    url = reverse("userprofile-list")
    response = client.get(url)
    assert response.status_code == expected_status
    assert len(response.data) == expected_length


@pytest.mark.parametrize(
    "client_fixture, expected_status",
    [
        ("authenticated_admin_client", status.HTTP_200_OK),
        ("authenticated_buyer_client", status.HTTP_403_FORBIDDEN),
        ("client", status.HTTP_401_UNAUTHORIZED),
    ],
)
def test_retrieve_user_profile(client_fixture, expected_status, request):
    client = request.getfixturevalue(client_fixture)
    user_profile = UserProfileFactory()
    url = reverse("userprofile-detail", args=[user_profile.id])
    response = client.get(url)
    assert response.status_code == expected_status
    if expected_status == status.HTTP_200_OK:
        assert response.data["name"] == user_profile.name


@pytest.mark.parametrize(
    "client_fixture, expected_status",
    [
        ("authenticated_admin_client", status.HTTP_200_OK),
        ("authenticated_buyer_client", status.HTTP_403_FORBIDDEN),
        ("client", status.HTTP_401_UNAUTHORIZED),
    ],
)
def test_update_user_profile(client_fixture, expected_status, request):
    client = request.getfixturevalue(client_fixture)
    user_profile = UserProfileFactory()
    url = reverse("userprofile-detail", args=[user_profile.id])
    data = {"name": "Updated User"}
    response = client.patch(url, data, format="json")
    assert response.status_code == expected_status
    if expected_status == status.HTTP_200_OK:
        user_profile.refresh_from_db()
        assert user_profile.name == "Updated User"


@pytest.mark.parametrize(
    "client_fixture, expected_status",
    [
        ("authenticated_admin_client", status.HTTP_204_NO_CONTENT),
        ("authenticated_buyer_client", status.HTTP_403_FORBIDDEN),
        ("client", status.HTTP_401_UNAUTHORIZED),
    ],
)
def test_delete_user_profile(client_fixture, expected_status, request):
    client = request.getfixturevalue(client_fixture)
    user_profile = UserProfileFactory()
    url = reverse("userprofile-detail", args=[user_profile.id])
    response = client.delete(url)
    assert response.status_code == expected_status
    if expected_status == status.HTTP_204_NO_CONTENT:
        assert not UserProfile.objects.filter(id=user_profile.id).exists()
