from django.test import TestCase
from apps.products.models import Product, Category


class ProductModelTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")

    def test_product_creation(self):
        name = "Test Product"
        price = 9.99
        product = Product.objects.create(name=name, price=price, category=self.category)

        self.assertEqual(product.name, name)
        self.assertEqual(float(product.price), price)
        self.assertEqual(product.category, self.category)

    def test_product_retrieval(self):
        name = "Test Product"
        product = Product.objects.create(name=name, price=9.99, category=self.category)

        retrieved_product = Product.objects.get(name=name)
        self.assertEqual(product, retrieved_product)

    def test_product_update(self):
        name = "Test Product"
        product = Product.objects.create(name=name, price=9.99, category=self.category)

        product.name = "Updated Product"
        product.save()

        updated_product = Product.objects.get(pk=product.pk)
        self.assertEqual(updated_product.name, "Updated Product")

    def test_product_deletion(self):
        name = "Test Product"
        product = Product.objects.create(name=name, price=9.99, category=self.category)

        product.delete()

        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get(name=name)

    def test_product_str_representation(self):
        name = "Test Product"
        product = Product.objects.create(name=name, price=9.99, category=self.category)

        self.assertEqual(str(product), name)
