from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import *
from rest_framework.generics import get_object_or_404
from django.utils.dateparse import parse_datetime
from django.db.models import Sum
from rest_framework.response import Response
from django.db.models import Q

from .models import Order
from apps.cafe.serializers import ListOrderItemsSerializer, ListOrderSerializer


class GetOrderItems:
    @permission_classes([IsAuthenticated])
    @action(["GET"], True, "order_items")
    def get_order_items(self, request, id, *args, **kwargs):

        queryset = get_object_or_404(self.get_queryset(), id=id)
        order_items = queryset.order_items.all()

        page = self.paginate_queryset(order_items)

        if page is not None:
            serializer = ListOrderItemsSerializer(
                page,
                many=True,
                context={"request": request},
            )
            return self.get_paginated_response(serializer.data)

        serializer = ListOrderItemsSerializer(
            order_items,
            many=True,
            context={"request": request},
        )

        return Response(serializer.data)


from datetime import timedelta

from django.utils.timezone import is_naive, make_aware


def process_datetime(value):
    if is_naive(value):
        return make_aware(value)
    return value


from django.utils.timezone import now


class GetRevenueAmount:
    @permission_classes([IsAuthenticated])
    @action(methods=["get"], detail=False, url_path="revenue")
    def get_revenue_amount(self, request, *args, **kwargs):
        start_time = request.query_params.get("start_time")
        end_time = request.query_params.get("end_time")

        if not start_time:
            return Response({"error": "Укажите start_time"}, status=400)

        try:
            start_time = parse_datetime(start_time)

            if not start_time:
                raise ValueError("Неверный формат даты и времени.")

        except ValueError as e:
            return Response({"error": str(e)}, status=400)

        # Обрабатываем наивные даты
        if start_time and is_naive(start_time):
            start_time = make_aware(start_time)

        # Если end_time не передан, используем текущее время
        if end_time:
            try:
                end_time = parse_datetime(end_time)
                if not end_time:
                    raise ValueError("Неверный формат end_time.")
            except ValueError as e:
                return Response({"error": str(e)}, status=400)

            # Обрабатываем наивные даты для end_time
            if end_time and is_naive(end_time):
                end_time = make_aware(end_time)
        else:
            end_time = now() + timedelta(hours=1)

        # Фильтруем заказы по диапазону времени
        orders = Order.objects.filter(created_at__range=(start_time, end_time)).filter(
            status=Order.PAID
        )

        serializer = ListOrderSerializer(orders, many=True)

        return Response(serializer.data)


class UpdateGetOrderStatus:

    @permission_classes([IsAuthenticated])
    @action(["PATCH"], True, "status")
    def update_status(self, request, id, *args, **kwargs):

        status = request.data.get("status")

        queryset = get_object_or_404(Order, id=id)

        if status in Order.STATUS:
            queryset.status = status
            queryset.save()
        else:
            return Response({"error": "Нет такого статуса"}, status=400)

        return Response({"default": f"Статус успешно изменён на {self.status}"})

    @permission_classes([IsAuthenticated])
    @action(["GET"], False, "status")
    def update_status(self, request, *args, **kwargs):

        return Response(
            {
                "PENDING": "В ожидании",
                "PAID": "Готово",
                "READY": "Оплачено",
            }
        )


class UpdateStatusListAction:

    @action(["POST"],False,"order_items")
    def update_status_list(self,request,*args, **kwargs):

        ...