from rest_framework import serializers

from .models import *


# Order
class ListOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = (
            "id",
            "table_number",
            "total_price",
            "owner",
            "status",
            "created_at",
            "updated_at",
        )


class RetrieveOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = "__all__"


class CreateOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = (
            "table_number",
            "status",
        )


# /Order/


# OrderItems
class DishOrderItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dish
        fields = (
            "image",
            "name",
        )


class ListOrderItemsSerializer(serializers.ModelSerializer):
    dish = DishOrderItemsSerializer()

    class Meta:
        model = OrderItem
        fields = (
            "id",
            "order",
            "dish",
            "price",
            "total_price",
            "count",
        )


# /OrderItems/
