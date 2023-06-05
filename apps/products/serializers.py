from rest_framework import serializers
from apps.products.models import Product
from apps.categories.models import Category
from apps.categories.serializers import CategorySerializer


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        source='category', write_only=True, queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'category', 'category_id')
