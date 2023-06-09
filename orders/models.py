from django.contrib.auth.models import User
from django.db import models

from products.models import Product


class Order(models.Model):
    order_number = models.PositiveIntegerField(unique=True, editable=False)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if not self.order_number:
            last_order = Order.objects.aggregate(models.Max("order_number"))
            last_order_number = last_order["order_number__max"]
            self.order_number = last_order_number + 1 if last_order_number else 1
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
