import pytest
from django.urls import reverse
from rest_framework import status

from .factories import CategoryDiscountFactory, CategoryFactory, ProductFactory
from products.models import Category, CategoryDiscount, Product

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "client_fixture, expected_status",
    [
        ("authenticated_admin_client", status.HTTP_200_OK),
        ("authenticated_buyer_client", status.HTTP_200_OK),
        ("client", status.HTTP_200_OK),
    ],
)
def test_list_categories(client_fixture, expected_status, request):
    client = request.getfixturevalue(client_fixture)
    CategoryFactory.create_batch(5)
    url = reverse("category-list")
    response = client.get(url)
    assert response.status_code == expected_status
    assert len(response.data) == 5


@pytest.mark.parametrize(
    "client_fixture, expected_status",
    [
        ("authenticated_admin_client", status.HTTP_200_OK),
        ("authenticated_buyer_client", status.HTTP_200_OK),
        ("client", status.HTTP_200_OK),
    ],
)
def test_retrieve_category(client_fixture, expected_status, request):
    client = request.getfixturevalue(client_fixture)
    category = CategoryFactory()
    url = reverse("category-detail", args=[category.id])
    response = client.get(url)
    assert response.status_code == expected_status
    assert response.data["name"] == category.name


@pytest.mark.parametrize(
    "client_fixture, expected_status, expected_create",
    [
        ("authenticated_admin_client", status.HTTP_201_CREATED, True),
        ("authenticated_buyer_client", status.HTTP_403_FORBIDDEN, False),
        ("client", status.HTTP_401_UNAUTHORIZED, False),
    ],
)
def test_create_category(client_fixture, expected_status, expected_create, request):
    client = request.getfixturevalue(client_fixture)
    data = {"name": "Test Category", "description": "Test Description"}
    url = reverse("category-list")
    response = client.post(url, data, format="json")
    assert response.status_code == expected_status
    assert Category.objects.filter(name="Test Category").exists() is expected_create


@pytest.mark.parametrize(
    "client_fixture, expected_status, expected_name",
    [
        ("authenticated_admin_client", status.HTTP_200_OK, "Updated Category"),
        ("authenticated_buyer_client", status.HTTP_403_FORBIDDEN, "Category Test"),
        ("client", status.HTTP_401_UNAUTHORIZED, "Category Test"),
    ],
)
def test_update_category(client_fixture, expected_status, expected_name, request):
    client = request.getfixturevalue(client_fixture)
    category = CategoryFactory(name="Category Test")
    data = {"name": "Updated Category"}
    url = reverse("category-detail", args=[category.id])
    response = client.patch(url, data, format="json")
    assert response.status_code == expected_status
    category.refresh_from_db()
    assert category.name == expected_name


@pytest.mark.parametrize(
    "client_fixture, expected_status, expected_delete",
    [
        ("authenticated_admin_client", status.HTTP_204_NO_CONTENT, False),
        ("authenticated_buyer_client", status.HTTP_403_FORBIDDEN, True),
        ("client", status.HTTP_401_UNAUTHORIZED, True),
    ],
)
def test_delete_category(client_fixture, expected_status, expected_delete, request):
    client = request.getfixturevalue(client_fixture)
    category = CategoryFactory()
    url = reverse("category-detail", args=[category.id])
    response = client.delete(url)
    assert response.status_code == expected_status
    assert Category.objects.filter(id=category.id).exists() is expected_delete


@pytest.mark.parametrize(
    "client_fixture, expected_status",
    [
        ("authenticated_admin_client", status.HTTP_200_OK),
        ("authenticated_buyer_client", status.HTTP_200_OK),
        ("client", status.HTTP_200_OK),
    ],
)
def test_list_products(client_fixture, expected_status, request):
    client = request.getfixturevalue(client_fixture)
    ProductFactory.create_batch(5)
    url = reverse("product-list")
    response = client.get(url)
    assert response.status_code == expected_status
    assert len(response.data) == 5


@pytest.mark.parametrize(
    "client_fixture, expected_status",
    [
        ("authenticated_admin_client", status.HTTP_200_OK),
        ("authenticated_buyer_client", status.HTTP_200_OK),
        ("client", status.HTTP_200_OK),
    ],
)
def test_retrieve_product(client_fixture, expected_status, request):
    client = request.getfixturevalue(client_fixture)
    product = ProductFactory()
    url = reverse("product-detail", args=[product.id])
    response = client.get(url)
    assert response.status_code == expected_status
    assert response.data["name"] == product.name


@pytest.mark.parametrize(
    "client_fixture, expected_status, expected_create",
    [
        ("authenticated_admin_client", status.HTTP_201_CREATED, True),
        ("authenticated_buyer_client", status.HTTP_403_FORBIDDEN, False),
        ("client", status.HTTP_401_UNAUTHORIZED, False),
    ],
)
def test_create_product(client_fixture, expected_status, expected_create, request):
    client = request.getfixturevalue(client_fixture)
    data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": 19.99,
        "image": "https://test.com/image.jpg",
    }
    url = reverse("product-list")
    response = client.post(url, data, format="json")
    assert response.status_code == expected_status
    assert Product.objects.filter(name="Test Product").exists() is expected_create


@pytest.mark.parametrize(
    "client_fixture, expected_status, expected_name",
    [
        ("authenticated_admin_client", status.HTTP_200_OK, "Updated Product"),
        ("authenticated_buyer_client", status.HTTP_403_FORBIDDEN, "Product Test"),
        ("client", status.HTTP_401_UNAUTHORIZED, "Product Test"),
    ],
)
def test_update_product(client_fixture, expected_status, expected_name, request):
    client = request.getfixturevalue(client_fixture)
    product = ProductFactory(name="Product Test")
    data = {"name": "Updated Product"}
    url = reverse("product-detail", args=[product.id])
    response = client.patch(url, data, format="json")
    assert response.status_code == expected_status
    product.refresh_from_db()
    assert product.name == expected_name


@pytest.mark.parametrize(
    "client_fixture, expected_status, expected_delete",
    [
        ("authenticated_admin_client", status.HTTP_204_NO_CONTENT, False),
        ("authenticated_buyer_client", status.HTTP_403_FORBIDDEN, True),
        ("client", status.HTTP_401_UNAUTHORIZED, True),
    ],
)
def test_delete_product(client_fixture, expected_status, expected_delete, request):
    client = request.getfixturevalue(client_fixture)
    product = ProductFactory()
    url = reverse("product-detail", args=[product.id])
    response = client.delete(url)
    assert response.status_code == expected_status
    assert Product.objects.filter(id=product.id).exists() is expected_delete


@pytest.mark.parametrize(
    "client_fixture, expected_status",
    [
        ("authenticated_admin_client", status.HTTP_200_OK),
        ("authenticated_buyer_client", status.HTTP_200_OK),
        ("client", status.HTTP_200_OK),
    ],
)
def test_list_category_discounts(client_fixture, expected_status, request):
    client = request.getfixturevalue(client_fixture)
    CategoryDiscountFactory.create_batch(5)
    url = reverse("categorydiscount-list")
    response = client.get(url)
    assert response.status_code == expected_status
    assert len(response.data) == 5


@pytest.mark.parametrize(
    "client_fixture, expected_status",
    [
        ("authenticated_admin_client", status.HTTP_200_OK),
        ("authenticated_buyer_client", status.HTTP_200_OK),
        ("client", status.HTTP_200_OK),
    ],
)
def test_retrieve_category_discount(client_fixture, expected_status, request):
    client = request.getfixturevalue(client_fixture)
    category_discount = CategoryDiscountFactory()
    url = reverse("categorydiscount-detail", args=[category_discount.id])
    response = client.get(url)
    assert response.status_code == expected_status
    assert response.data["category"] == category_discount.category.id


@pytest.mark.parametrize(
    "client_fixture, expected_status, expected_create",
    [
        ("authenticated_admin_client", status.HTTP_201_CREATED, True),
        ("authenticated_buyer_client", status.HTTP_403_FORBIDDEN, False),
        ("client", status.HTTP_401_UNAUTHORIZED, False),
    ],
)
def test_create_category_discount(client_fixture, expected_status, expected_create, request):
    client = request.getfixturevalue(client_fixture)
    category = CategoryFactory()
    data = {
        "category": category.id,
        "discount_percentage": 20,
        "product_quantity": 10,
    }
    url = reverse("categorydiscount-list")
    response = client.post(url, data, format="json")
    assert response.status_code == expected_status
    assert CategoryDiscount.objects.filter(category=category).exists() is expected_create


@pytest.mark.parametrize(
    "client_fixture, expected_status, expected_discount",
    [
        ("authenticated_admin_client", status.HTTP_200_OK, 30),
        ("authenticated_buyer_client", status.HTTP_403_FORBIDDEN, 50),
        ("client", status.HTTP_401_UNAUTHORIZED, 50),
    ],
)
def test_update_category_discount(client_fixture, expected_status, expected_discount, request):
    client = request.getfixturevalue(client_fixture)
    category_discount = CategoryDiscountFactory(discount_percentage=50)
    data = {"discount_percentage": 30}
    url = reverse("categorydiscount-detail", args=[category_discount.id])
    response = client.patch(url, data, format="json")
    assert response.status_code == expected_status
    category_discount.refresh_from_db()
    assert category_discount.discount_percentage == expected_discount


@pytest.mark.parametrize(
    "client_fixture, expected_status, expected_delete",
    [
        ("authenticated_admin_client", status.HTTP_204_NO_CONTENT, False),
        ("authenticated_buyer_client", status.HTTP_403_FORBIDDEN, True),
        ("client", status.HTTP_401_UNAUTHORIZED, True),
    ],
)
def test_delete_category_discount(client_fixture, expected_status, expected_delete, request):
    client = request.getfixturevalue(client_fixture)
    category_discount = CategoryDiscountFactory()
    url = reverse("categorydiscount-detail", args=[category_discount.id])
    response = client.delete(url)
    assert response.status_code == expected_status
    assert CategoryDiscount.objects.filter(id=category_discount.id).exists() is expected_delete
