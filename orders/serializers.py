from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Order, OrderItem
from products.models import CategoryDiscount, Product
from products.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ("id", "product", "quantity", "unit_price", "discount_amount", "subtotal")


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    customer = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Order
        fields = ("id", "order_number", "customer", "total_amount", "order_items")


class OrderCreateSerializer(serializers.ModelSerializer):
    order_items = serializers.ListField(child=serializers.DictField())

    class Meta:
        model = OrderItem
        fields = ["order_items"]

    def create(self, validated_data):
        order = Order.objects.create(customer=self.context["request"].user)
        total_amount = 0

        for order_item_data in validated_data["order_items"]:
            product_id = order_item_data["product"]
            quantity = order_item_data["quantity"]

            product = Product.objects.get(pk=product_id)

            category_discount = (
                CategoryDiscount.objects.filter(
                    category__in=product.categories.all(), product_quantity__lte=quantity
                )
                .order_by("-discount_percentage")
                .first()
            )

            unit_price = product.price
            discount_amount = 0
            if category_discount:
                discount_amount = (unit_price * quantity * category_discount.discount_percentage) / 100
            subtotal = unit_price * quantity - discount_amount
            total_amount += subtotal

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                unit_price=unit_price,
                discount_amount=discount_amount,
                subtotal=subtotal,
            )

        order.total_amount = total_amount
        order.save()

        order_data = OrderSerializer(order).data
        return order_data
