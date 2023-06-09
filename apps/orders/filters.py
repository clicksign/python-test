from django_filters import FilterSet, CharFilter
from apps.orders.models import Order


class OrderFilter(FilterSet):
    user_id = CharFilter(field_name='user__id', lookup_expr='exact')
    user_name = CharFilter(field_name='user__username', lookup_expr='exact')

    class Meta:
        model = Order
        fields = ('user_id', 'user_name')
