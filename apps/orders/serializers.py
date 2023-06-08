from rest_framework import serializers

from apps.orders.models import Order, OrderItem
from apps.products.models import Product
from apps.products.serializers import ProductSerializer
from apps.users.serializers import CustomUserSerializer


class PercentageField(serializers.DecimalField):
    def to_representation(self, value):
        return f'{int(value)}%' if value else '0%'


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        source='product', write_only=True, queryset=Product.objects.all())
    discount = PercentageField(max_digits=5, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'product_id', 'quantity', 'discount', 'total')
        read_only_fields = ('discount', 'total')


class OrderSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    order_items = OrderItemSerializer(many=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'order_items', 'total')

    def create(self, validated_data):
        order_items = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)
        for order_item in order_items:
            OrderItem.objects.create(order=order, **order_item)

        order.recalculate_total()
        return order

    def update(self, instance, validated_data):
        order_items_data = validated_data.pop('order_items')
        instance = super().update(instance, validated_data)

        for order_item_data in order_items_data:
            try:
                order_item = OrderItem.objects.get(
                    order=instance, 
                    product=order_item_data['product']
                )
            except OrderItem.DoesNotExist:
                OrderItem.objects.create(order=instance, **order_item_data)
            else:
                order_item.quantity = order_item_data.get('quantity', order_item.quantity)
                order_item.save()

        instance.recalculate_total()
        return instance
