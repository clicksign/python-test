from django.urls import reverse


def test_order_urls():
    assert reverse("order-list") == "/v1/orders/"
    assert reverse("order-detail", args=[1]) == "/v1/orders/1/"


def test_order_item_urls():
    assert reverse("orderitem-list") == "/v1/order-items/"
    assert reverse("orderitem-detail", args=[1]) == "/v1/order-items/1/"
