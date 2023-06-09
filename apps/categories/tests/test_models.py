from django.test import TestCase
from apps.categories.models import Category


class CategoryModelTestCase(TestCase):
    def test_category_creation(self):
        category = Category.objects.create(name="Test Category")
        self.assertEqual(category.name, "Test Category")

    def test_category_retrieval(self):
        category = Category.objects.create(name="Test Category")
        retrieved_category = Category.objects.get(name="Test Category")
        self.assertEqual(category, retrieved_category)

    def test_category_update(self):
        category = Category.objects.create(name="Test Category")
        category.name = "Updated Category"
        category.save()

        updated_category = Category.objects.get(pk=category.pk)
        self.assertEqual(updated_category.name, "Updated Category")

    def test_category_deletion(self):
        category = Category.objects.create(name="Test Category")
        category.delete()

        with self.assertRaises(Category.DoesNotExist):
            Category.objects.get(name="Test Category")

    def test_category_str_representation(self):
        category = Category.objects.create(name="Test Category")
        self.assertEqual(str(category), "Test Category")
