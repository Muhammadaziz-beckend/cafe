from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.utils.timezone import datetime

from .models import Order, OrderItem


# @receiver(m2m_changed, sender=Order.items.through)
# def update_total_price(sender, instance: Order, action, **kwargs):
#     """
#     Сигнал для автоматического вычисления цены
#     """
#     if action in ["post_add", "post_remove", "post_clear"]:
#         try:
#             instance.total_price = sum(item.price for item in instance.items.all())
#             instance.save()
#         except Exception as e:
#             print(f"Ошибка при пересчете стоимости заказа: {e}")


@receiver(post_save, sender=OrderItem)
def update_price_order_item(sender, instance: OrderItem, created, **kwargs):

    if created or (
        datetime.now().date() == instance.created_at.date()
        and datetime.now().year == instance.created_at.year
    ):

        dish = instance.dish
        total_price = dish.price * instance.count

        if total_price != instance.total_price:
            instance.total_price = total_price
            instance.price = dish.price
            instance.save()
            instance.order.save()


@receiver(post_save, sender=Order)
def update_price_order(sender, instance: Order, created, **kwargs):

    if created or (
        datetime.now().date() == instance.created_at.date()
        and datetime.now().year == instance.created_at.year
    ):

        order_items_total_price = sum(
            [i.price * i.count for i in instance.order_items.all()]
        )
        print(
            instance.total_price,
            order_items_total_price,
            instance.total_price != order_items_total_price,
        )
        if instance.total_price != order_items_total_price:
            instance.total_price = order_items_total_price
            instance.save()
