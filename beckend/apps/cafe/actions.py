from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import *
from rest_framework.generics import get_object_or_404
from django.utils.dateparse import parse_datetime
from django.db.models import Sum
from rest_framework.response import Response

from .models import Order
from apps.cafe.serializers import ListOrderItemsSerializer


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


class GetRevenueAmount:

    @permission_classes(IsAuthenticated)
    @action(["GET"], False, "revenue")
    def get_revenue_amount(self, request, *args, **kwargs):

        start_time = request.query_params.get("start_time")
        end_time = request.query_params.get("end_time")

        if not start_time or not end_time:
            return Response({"error": "Укажите start_time и end_time"}, status=400)

        try:
            start_time = parse_datetime(start_time)
            end_time = parse_datetime(end_time)

            if not start_time or not end_time:
                raise ValueError("Неверный формат даты и времени.")

        except ValueError as e:
            return Response({"error": str(e)}, status=400)

        orders = Order.objects.filter(
            status=Order.PAID,
            created_at__gte=start_time,
            created_at__lte=end_time,
        )

        total_revenue = orders.aggregate(total=Sum("total_price"))["total"] or 0

        return Response(
            {
                "start_time": start_time,
                "end_time": end_time,
                "total_revenue": total_revenue,
            }
        )


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
