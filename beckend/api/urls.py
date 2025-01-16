from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.account.views import *
from apps.cafe.views import *

from .ysge import swagger

router = DefaultRouter()
router.register("orders", OrdersViewSet)
router.register("orders_items", OrderItemsViewSet)
router.register("dish", DishViewSet)

urlpatterns = [
    # auth
    path("auth/login/", Login.as_view()),
    path("auth/create_employee/", CreateEmployee.as_view()),
    path("auth/cheng_password/", UpdatePasswordUser.as_view()),
    #
    path("", include(router.urls)),
]

urlpatterns += swagger
