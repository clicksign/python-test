from django.db import models
from django.db.models import ProtectedError


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        try:
            products = self.product_set.all().values_list('id', flat=True)
            if products:
                raise ProtectedError("Category is associated with products and cannot be deleted.", products)
            super().delete(*args, **kwargs)
        except ProtectedError as e:
            raise e
