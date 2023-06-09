import pytest
from django.db.models import Max

from .factories import OrderFactory, OrderItemFactory
from orders.models import Order, OrderItem

pytestmark = pytest.mark.django_db


def test_order_creation():
    order = OrderFactory()
    assert isinstance(order, Order)
    assert Order.objects.count() == 1


def test_order_item_creation():
    order_item = OrderItemFactory()
    assert isinstance(order_item, OrderItem)
    assert OrderItem.objects.count() == 1


def test_order_save_order_number():
    max_order_number = Order.objects.aggregate(Max("order_number"))["order_number__max"]
    order = OrderFactory(order_number=None)

    expected_order_number = max_order_number + 1 if max_order_number else 1
    assert order.order_number == expected_order_number
