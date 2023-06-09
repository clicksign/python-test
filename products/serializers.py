from rest_framework import serializers

from .models import Category, CategoryDiscount, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CategoryDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryDiscount
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    category_discounts = CategoryDiscountSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"
