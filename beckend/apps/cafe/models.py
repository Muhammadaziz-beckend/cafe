from django.db import models
from django_resized import ResizedImageField

from utils.models import DateTimeAbstract


class Order(DateTimeAbstract):
    PENDING = "pending"
    PAID = "paid"
    READY = "ready"

    STATUS = (PENDING, PAID, READY)

    STATUS_CHOICES = [
        (PENDING, "В ожидании"),
        (READY, "Готово"),
        (PAID, "Оплачено"),
    ]

    table_number = models.IntegerField("номер стола")
    total_price = models.DecimalField(
        "Общая цена",
        max_digits=10,
        decimal_places=2,
        default=0.0,
    )
    owner = models.ForeignKey(
        "account.User",
        models.SET_NULL,
        null=True,
        verbose_name="Кассир",
        related_name="orders",
    )
    status = models.CharField(
        "Статус",
        choices=STATUS_CHOICES,
        max_length=7,
        default=PENDING,
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"id:{self.pk} status:{self.status}"


class Dish(models.Model):
    image = ResizedImageField(
        "Изображения",
        size=[600, 600],
        upload_to="dish/",
        force_format="WEBP",
        quality=90,
        null=True,
        blank=True,
    )
    name = models.CharField(
        "Названия блюдо",
        max_length=120,
    )
    price = models.DecimalField(
        "Цена",
        max_digits=10,
        decimal_places=2,
    )

    class Meta:
        verbose_name = "блюдо"
        verbose_name_plural = "блюда"

    def __str__(self):
        return self.name


class OrderItem(DateTimeAbstract):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="order_items",
        verbose_name="Заказ",
    )
    dish = models.ForeignKey(
        Dish,
        on_delete=models.CASCADE,
        related_name="order_items",
        verbose_name="Блюдо",
    )
    price = models.DecimalField(
        "Цена",
        max_digits=10,
        decimal_places=2,
        default=0.0,
    )
    total_price = models.DecimalField(
        "Общая сумма Цена",
        max_digits=10,
        decimal_places=2,
        default=0.0,
    )
    count = models.PositiveIntegerField(
        "Количество",
        default=1,
    )

    class Meta:
        verbose_name = "Элемент заказа"
        verbose_name_plural = "Элементы заказа"

    def __str__(self):
        return f"{self.dish.name} x {self.count}"
