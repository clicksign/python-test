from django_filters import FilterSet, CharFilter
from apps.products.models import Product


class ProductFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')
    category = CharFilter(field_name='category__name', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ('name', 'category')
