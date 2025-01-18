from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
from apps.account.models import User

from .models import *


# Order
class OwnerUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = (
            "id",
            "username",
        )



class ListOrderSerializer(serializers.ModelSerializer):
    owner = OwnerUserSerializer()

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
            "id",
            "table_number",
            "status",
        )

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user
        validated_data["owner"] = user
        return super().create(validated_data)


# /Order/


# OrderItems


class DishOrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = (
            "id",
            "image",
            "name",
        )  # Укажите нужные поля


class OrderOrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = "__all__"


class ListOrderItemsSerializer(WritableNestedModelSerializer):
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


class RetrieveOrderItemsSerializer(serializers.ModelSerializer):
    dish = DishOrderItemsSerializer()
    order = OrderOrderItemSerializer()

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


class ListCreateOrderItemsSerializer(serializers.Serializer):
    dish_id = serializers.PrimaryKeyRelatedField(queryset=Dish.objects.all())
    count = serializers.IntegerField()


class CreteOrderItemsSerializer(serializers.ModelSerializer):
    order_id = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())
    products = ListCreateOrderItemsSerializer(many=True)

    class Meta:
        model = OrderItem
        fields = ("order_id", "products")

    def create(self, validated_data):
        products_data = validated_data.get("products")
        check_product = validated_data["order_id"]

        for product_data in products_data:
            OrderItem.objects.create(
                order=check_product,
                dish=product_data["dish_id"],
                count=product_data["count"],
            )

        return validated_data


class UpdateOrderItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = (
            "order",
            "dish",
            "count",
        )


# /OrderItems/

# Dish


class ListDishSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dish
        fields = "__all__"


class CreateDishSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dish
        fields = (
            "image",
            "name",
            "price",
        )


# class RetrieveDishSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Dish
#         fields = "__all__"

# /Dish/
