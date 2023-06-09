import pytest

from .factories import CategoryDiscountFactory, CategoryFactory, ProductFactory
from products.models import Category, CategoryDiscount, Product

pytestmark = pytest.mark.django_db


def test_category_creation():
    category = CategoryFactory()
    assert isinstance(category, Category)
    assert Category.objects.count() == 1


def test_category_discount_creation():
    category_discount = CategoryDiscountFactory()
    assert isinstance(category_discount, CategoryDiscount)
    assert CategoryDiscount.objects.count() == 1


def test_product_creation():
    product = ProductFactory()
    assert isinstance(product, Product)
    assert Product.objects.count() == 1


def test_product_categories():
    category1 = CategoryFactory()
    category2 = CategoryFactory()
    product = ProductFactory(categories=[category1, category2])

    assert product.categories.count() == 2
    assert category1 in product.categories.all()
    assert category2 in product.categories.all()
