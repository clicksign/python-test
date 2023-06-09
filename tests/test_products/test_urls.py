from django.urls import reverse


def test_category_urls():
    assert reverse("category-list") == "/v1/categories/"
    assert reverse("category-detail", args=[1]) == "/v1/categories/1/"


def test_category_discount_urls():
    assert reverse("categorydiscount-list") == "/v1/category-discounts/"
    assert reverse("categorydiscount-detail", args=[1]) == "/v1/category-discounts/1/"


def test_product_urls():
    assert reverse("product-list") == "/v1/products/"
    assert reverse("product-detail", args=[1]) == "/v1/products/1/"
