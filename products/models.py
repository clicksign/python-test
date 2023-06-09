from django.core.validators import MaxValueValidator
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()


class CategoryDiscount(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="discounts")
    discount_percentage = models.IntegerField(validators=[MaxValueValidator(100)])
    product_quantity = models.IntegerField()


class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    categories = models.ManyToManyField(Category)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField()
