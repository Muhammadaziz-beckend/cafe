from django_filters import rest_framework as filters

from .models import Order, OrderItem


class OrderFilter(filters.FilterSet):

    class Meta:
        model = Order
        fields = (
            "owner",
            "status",
        )


class OrderItemsFilter(filters.FilterSet):

    class Meta:
        model = OrderItem
        fields = (
            "order",
            "dish",
            "count",
        )
