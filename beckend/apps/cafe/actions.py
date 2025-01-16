from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import *
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

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
