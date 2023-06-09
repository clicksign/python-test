import pytest
from django.forms.models import model_to_dict

from .factories import CategoryDiscountFactory, CategoryFactory, ProductFactory
from products.serializers import CategoryDiscountSerializer, CategorySerializer, ProductSerializer

pytestmark = pytest.mark.django_db


def test_valid_category_serializer():
    category = CategoryFactory()
    serializer = CategorySerializer(data=model_to_dict(category))
    assert serializer.is_valid() is True


def test_invalid_category_serializer():
    serializer = CategorySerializer(data={})
    assert serializer.is_valid() is False
    assert "name" in serializer.errors
    assert "description" in serializer.errors


def test_valid_category_discount_serializer():
    category_discount = CategoryDiscountFactory()
    serializer = CategoryDiscountSerializer(data=model_to_dict(category_discount))
    assert serializer.is_valid() is True


def test_invalid_category_discount_serializer():
    serializer = CategoryDiscountSerializer(data={})
    assert serializer.is_valid() is False
    assert "category" in serializer.errors
    assert "discount_percentage" in serializer.errors
    assert "product_quantity" in serializer.errors


def test_valid_product_serializer():
    product = ProductFactory()
    serializer = ProductSerializer(data=model_to_dict(product))
    assert serializer.is_valid() is True


def test_invalid_product_serializer():
    serializer = ProductSerializer(data={})
    assert serializer.is_valid() is False
    assert "name" in serializer.errors
    assert "description" in serializer.errors
    assert "price" in serializer.errors
    assert "image" in serializer.errors
