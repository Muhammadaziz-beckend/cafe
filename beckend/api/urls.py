from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.cafe.views import OrdersViewSet

from .ysge import swagger

router = DefaultRouter()
router.register("orders",OrdersViewSet)

urlpatterns = [
    #
    path("", include(router.urls)),
]

urlpatterns += swagger
