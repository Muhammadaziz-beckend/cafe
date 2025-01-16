from rest_framework.permissions import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from apps.cafe.actions import GetOrderItems
from apps.cafe.filters import OrderFilter
from apps.cafe.serializers import *
from utils.mixins import UltraModelViewSet
from utils.permissions import IsOwner
from .models import Order, OrderItem


class OrdersViewSet(GetOrderItems,UltraModelViewSet):
    queryset = Order.objects.all()
    lookup_field = "id"
    filter_backends = [OrderingFilter, SearchFilter, DjangoFilterBackend]
    filterset_class = OrderFilter
    ordering_fields = ["created_at"]
    search_fields = ["table_number"]
    serializer_classes = {
        "list": ListOrderSerializer,
        "retrieve": RetrieveOrderSerializer,
        "create": CreateOrderSerializer,
        "update": CreateOrderSerializer,
    }
    permission_classes_by_action = {
        "list": [IsAuthenticated],
        "retrieve": [IsAuthenticated],
        "create": [IsAuthenticated],
        "update": [IsAuthenticated, IsOwner | IsAdminUser],
    }
