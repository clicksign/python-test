import pytest
from django.test import RequestFactory

from .factories import OrderFactory, OrderItemFactory
from orders.models import OrderItem
from orders.serializers import OrderCreateSerializer, OrderItemSerializer, OrderSerializer
from tests.test_products.factories import CategoryDiscountFactory, CategoryFactory, ProductFactory
from tests.test_users.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_valid_order_item_serializer():
    product = ProductFactory()
    order_item = OrderItemFactory(product=product)
    serialized_data = OrderItemSerializer(order_item).data
    serializer = OrderItemSerializer(data=serialized_data)
    assert serializer.is_valid() is True


def test_valid_order_serializer():
    customer = UserFactory()
    order = OrderFactory(customer=customer)
    serialized_data = OrderSerializer(order).data
    serializer = OrderSerializer(data=serialized_data)
    assert serializer.is_valid() is True


def test_valid_order_create_serializer():
    product = ProductFactory()
    data = {"order_items": [{"product": product.pk, "quantity": 5}]}
    serializer = OrderCreateSerializer(data=data)
    assert serializer.is_valid() is True


def test_invalid_order_create_serializer():
    serializer = OrderCreateSerializer(data={})
    assert serializer.is_valid() is False
    assert "order_items" in serializer.errors


def test_order_create_serializer_create():
    user = UserFactory()
    category1 = CategoryFactory()
    product1 = ProductFactory(price=10, categories=[category1])

    category2 = CategoryFactory()
    product2 = ProductFactory(price=20, categories=[category2])

    category3 = CategoryFactory()
    product3 = ProductFactory(price=5, categories=[category3])

    product4 = ProductFactory(price=8)

    CategoryDiscountFactory(category=category1, product_quantity=2, discount_percentage=10)
    CategoryDiscountFactory(category=category2, product_quantity=1, discount_percentage=20)
    CategoryDiscountFactory(category=category3, product_quantity=10, discount_percentage=50)

    request = RequestFactory().post("/")
    request.user = user

    serializer = OrderCreateSerializer(context={"request": request})

    validated_data = {
        "order_items": [
            {
                "product": product1.pk,
                "quantity": 2,
            },
            {
                "product": product2.pk,
                "quantity": 1,
            },
            {
                "product": product3.pk,
                "quantity": 2,
            },
            {
                "product": product4.pk,
                "quantity": 1,
            },
        ]
    }

    order = serializer.create(validated_data)

    order_items = OrderItem.objects.filter(order=order["id"])
    assert len(order_items) == len(validated_data["order_items"])
    assert order["total_amount"] == "52.00"
