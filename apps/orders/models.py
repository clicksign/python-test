from django.conf import settings
from django.db import models

from apps.products.models import Product
from apps.discounts.services import DiscountService


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def recalculate_total(self):
        self.total = 0
        self.total = sum([order_item.total for order_item in self.order_items.all()])
        self.save()

    def __str__(self):
        return f'Order - {self.id}'


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='order_items'
    )
    quantity = models.PositiveIntegerField()
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_items'
    )
    discount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return f'{self.product.name} - {self.quantity}'

    def save(self, *args, **kwargs):
        self.discount = DiscountService.calculate_discount(self.product.category.id, self.quantity)
        self.total = self.product.price * self.quantity
        self.total = self.total - (self.total * self.discount / 100)
        super().save(*args, **kwargs)
