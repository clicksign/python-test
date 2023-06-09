from django.db import models
from apps.categories.models import Category


class Discount(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    mininum_quantity = models.PositiveIntegerField()
    discount = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f'{self.category.name} - {self.discount}%'
