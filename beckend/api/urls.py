from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.cafe.views import *

from .ysge import swagger

router = DefaultRouter()
router.register("orders",OrdersViewSet)
router.register("orders_items",OrderItemsViewSet)
router.register("dish",DishViewSet)

urlpatterns = [
    #
    path("", include(router.urls)),
]

urlpatterns += swagger
