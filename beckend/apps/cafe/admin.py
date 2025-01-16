from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "table_number",
        "owner",
        "total_price",
        "status",
        "created_at",
        "updated_at",
    )

    list_display_links = (
        "id",
        "table_number",
        "owner",
        "total_price",
        "created_at",
        "updated_at",
    )

    list_editable = ("status",)

    list_filter = (
        "status",
        "created_at",
    )

    readonly_fields = ("total_price",)


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "price",
        "get_image",
    )

    list_display_links = (
        "id",
        "name",
        "price",
        "get_image",
    )

    @admin.display(description="Изображения блюда")
    def get_image(self, dish: Dish):
        if dish:
            return mark_safe(
                f'<img src="{dish.image.url}" alt="{dish.name}" width="100px" />'
            )
        return "-"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "order",
        "dish",
        "price",
        "total_price",
        "count",
        "created_at",
        "updated_at",
    )

    list_display_links = (
        "id",
        "order",
        "dish",
        "price",
        "total_price",
        "count",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "order",
        "dish",
    )

    readonly_fields = ("price", "total_price")
