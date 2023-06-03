from django.db import models
from django.db.models import ProtectedError
from apps.categories.models import Category


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        try:
            orders = self.order_items.all().values_list('order_id', flat=True)
            if orders:
                raise ProtectedError("Product is associated with orders and cannot be deleted.", orders)
            super().delete(*args, **kwargs)
        except ProtectedError as e:
            raise e
