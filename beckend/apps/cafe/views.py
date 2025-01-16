from rest_framework.permissions import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .actions import *
from .filters import *
from .serializers import *
from utils.mixins import UltraModelViewSet
from utils.permissions import IsOwner
from .models import Order, OrderItem


class OrdersViewSet(
    UpdateGetOrderStatus,
    GetRevenueAmount,
    GetOrderItems,
    UltraModelViewSet,
):
    queryset = Order.objects.all().order_by("-created_at")
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
        "destroy": [IsAuthenticated, IsOwner | IsAdminUser],
    }


class OrderItemsViewSet(UltraModelViewSet):
    queryset = OrderItem.objects.all().order_by("-created_at")
    lookup_field = "id"
    filter_backends = [OrderingFilter, SearchFilter, DjangoFilterBackend]
    ordering_fields = ["created_at", "count"]
    search_fields = ["count"]
    filterset_class = OrderItemsFilter
    serializer_classes = {
        "list": ListOrderItemsSerializer,
        "retrieve": RetrieveOrderItemsSerializer,
        "create": CreteOrderItemsSerializer,
        "update": UpdateOrderItemsSerializer,
    }
    permission_classes_by_action = {
        "list": [IsAuthenticated],
        "retrieve": [IsAuthenticated],
        "create": [IsAuthenticated],
        "update": [IsAuthenticated, IsOwner | IsAdminUser],
        "destroy": [IsAuthenticated, IsOwner | IsAdminUser],
    }


class DishViewSet(UltraModelViewSet):
    queryset = Dish.objects.all()
    lookup_field = "id"
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ["price"]
    search_fields = ["name", "price"]
    serializer_classes = {
        "list": ListDishSerializer,
        "retrieve": ListDishSerializer,
        "create": CreateDishSerializer,
        "update": CreateDishSerializer,
    }
    permission_classes_by_action = {
        "list": [IsAuthenticated],
        "retrieve": [IsAuthenticated],
        "create": [IsAuthenticated],
        "update": [IsAuthenticated, IsAdminUser],
        "destroy": [IsAuthenticated, IsAdminUser],
    }
