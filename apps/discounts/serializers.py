from rest_framework import serializers
from apps.discounts.models import Discount
from apps.orders.serializers import PercentageField


class DiscountSerializer(serializers.ModelSerializer):
    discount = PercentageField(max_digits=5, decimal_places=2)

    class Meta:
        model = Discount
        fields = ('id', 'category', 'mininum_quantity', 'discount')
