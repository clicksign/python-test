from decimal import Decimal

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .factories import OrderFactory, OrderItemFactory
from orders.models import Order, OrderItem
from tests.test_products.factories import ProductFactory
from tests.test_users.factories import UserProfileFactory

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "client_fixture, expected_status, expected_count",
    [
        ("authenticated_admin_client", status.HTTP_200_OK, 5),
        ("authenticated_buyer_client", status.HTTP_403_FORBIDDEN, 1),
        ("client", status.HTTP_401_UNAUTHORIZED, 1),
    ],
)
def test_list_orders(client_fixture, expected_status, expected_count, request):
    client = request.getfixturevalue(client_fixture)
    OrderFactory.create_batch(5)
    url = reverse("order-list")
    response = client.get(url)
    assert response.status_code == expected_status
    assert len(response.data) == expected_count


@pytest.mark.parametrize(
    "client_fixture, expected_status, expected_id",
    [
        ("authenticated_admin_client", status.HTTP_200_OK, 1),
        ("authenticated_buyer_client", status.HTTP_403_FORBIDDEN, None),
        ("client", status.HTTP_401_UNAUTHORIZED, None),
    ],
)
def test_retrieve_order(client_fixture, expected_status, expected_id, request):
    client = request.getfixturevalue(client_fixture)
    order = OrderFactory()
    url = reverse("order-detail", args=[order.pk])
    response = client.get(url)
    assert response.status_code == expected_status
    assert response.data.get("id") is expected_id


def test_retrieve_order_buyer_order():
    client = APIClient()
    user_profile = UserProfileFactory()
    token = Token.objects.create(user=user_profile.user)
    client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

    order = OrderFactory(customer=user_profile.user)
    url = reverse("order-detail", args=[order.pk])
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data.get("id") == order.id


@pytest.mark.parametrize(
    "client_fixture, expected_status, expected_count",
    [
        ("authenticated_admin_client", status.HTTP_201_CREATED, 1),
        ("authenticated_buyer_client", status.HTTP_201_CREATED, 1),
        ("client", status.HTTP_401_UNAUTHORIZED, 0),
    ],
)
def test_create_order(client_fixture, expected_status, expected_count, request):
    client = request.getfixturevalue(client_fixture)
    product = ProductFactory()
    url = reverse("order-list")
    data = {
        "order_items": [
            {
                "product": product.id,
                "quantity": 1,
            }
        ]
    }
    response = client.post(url, data, format="json")
    assert response.status_code == expected_status
    assert Order.objects.count() == expected_count


@pytest.mark.parametrize(
    "client_fixture, expected_status, expected_total_amount",
    [
        ("authenticated_admin_client", status.HTTP_200_OK, 100),
        ("authenticated_buyer_client", status.HTTP_403_FORBIDDEN, 10),
        ("client", status.HTTP_401_UNAUTHORIZED, 10),
    ],
)
def test_update_order(client_fixture, expected_status, expected_total_amount, request):
    client = request.getfixturevalue(client_fixture)
    order = OrderFactory(total_amount="10")
    url = reverse("order-detail", args=[order.pk])
    data = {"total_amount": Decimal("100.00")}
    response = client.patch(url, data, format="json")
    assert response.status_code == expected_status
    order.refresh_from_db()
    assert order.total_amount == expected_total_amount


@pytest.mark.parametrize(
    "client_fixture, expected_status, expected_delete",
    [
        ("authenticated_admin_client", status.HTTP_204_NO_CONTENT, False),
        ("authenticated_buyer_client", status.HTTP_403_FORBIDDEN, True),
        ("client", status.HTTP_401_UNAUTHORIZED, True),
    ],
)
def test_delete_order(client_fixture, expected_status, expected_delete, request):
    order = OrderFactory()
    client = request.getfixturevalue(client_fixture)
    url = reverse("order-detail", args=[order.pk])
    response = client.delete(url)
    assert response.status_code == expected_status
    assert Order.objects.filter(pk=order.pk).exists() is expected_delete


@pytest.mark.parametrize(
    "client_fixture, expected_status, expected_count",
    [
        ("authenticated_admin_client", status.HTTP_200_OK, 5),
        ("authenticated_buyer_client", status.HTTP_403_FORBIDDEN, 1),
        ("client", status.HTTP_401_UNAUTHORIZED, 1),
    ],
)
def test_list_order_items(client_fixture, expected_status, expected_count, request):
    client = request.getfixturevalue(client_fixture)
    order = OrderFactory()
    OrderItemFactory.create_batch(5, order=order)
    url = reverse("orderitem-list")
    response = client.get(url)
    assert response.status_code == expected_status
    assert len(response.data) == expected_count


@pytest.mark.parametrize(
    "client_fixture, expected_status, expected_id",
    [
        ("authenticated_admin_client", status.HTTP_200_OK, 1),
        ("authenticated_buyer_client", status.HTTP_403_FORBIDDEN, None),
        ("client", status.HTTP_401_UNAUTHORIZED, None),
    ],
)
def test_retrieve_order_item(client_fixture, expected_status, expected_id, request):
    client = request.getfixturevalue(client_fixture)
    order_item = OrderItemFactory()
    url = reverse("orderitem-detail", args=[order_item.pk])
    response = client.get(url)
    assert response.status_code == expected_status
    assert response.data.get("id") is expected_id


@pytest.mark.parametrize(
    "client_fixture, expected_status",
    [
        ("authenticated_admin_client", status.HTTP_403_FORBIDDEN),
        ("authenticated_buyer_client", status.HTTP_403_FORBIDDEN),
        ("client", status.HTTP_401_UNAUTHORIZED),
    ],
)
def test_create_order_item(client_fixture, expected_status, request):
    client = request.getfixturevalue(client_fixture)
    url = reverse("orderitem-list")
    data = {
        "order": 1,
    }
    response = client.post(url, data, format="json")
    assert response.status_code == expected_status
    assert OrderItem.objects.count() == 0


@pytest.mark.parametrize(
    "client_fixture, expected_status, expected_quantity",
    [
        ("authenticated_admin_client", status.HTTP_200_OK, 5),
        ("authenticated_buyer_client", status.HTTP_403_FORBIDDEN, 1),
        ("client", status.HTTP_401_UNAUTHORIZED, 1),
    ],
)
def test_update_order_item(client_fixture, expected_status, expected_quantity, request):
    client = request.getfixturevalue(client_fixture)
    order_item = OrderItemFactory(quantity=1)
    url = reverse("orderitem-detail", args=[order_item.pk])
    data = {"quantity": 5}
    response = client.patch(url, data, format="json")
    assert response.status_code == expected_status
    order_item.refresh_from_db()
    assert order_item.quantity == expected_quantity


@pytest.mark.parametrize(
    "client_fixture, expected_status, expected_delete",
    [
        ("authenticated_admin_client", status.HTTP_204_NO_CONTENT, False),
        ("authenticated_buyer_client", status.HTTP_403_FORBIDDEN, True),
        ("client", status.HTTP_401_UNAUTHORIZED, True),
    ],
)
def test_delete_order_item(client_fixture, expected_status, expected_delete, request):
    order_item = OrderItemFactory()
    client = request.getfixturevalue(client_fixture)
    url = reverse("orderitem-detail", args=[order_item.pk])
    response = client.delete(url)
    assert response.status_code == expected_status
    assert OrderItem.objects.filter(pk=order_item.pk).exists() is expected_delete
