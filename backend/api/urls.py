from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .orders.views import OrderViewSet
from .users.views import CustomerViewSet
from .delivery_points.views import (
    AreaViewSet,
    StreetViewSet,
    DeliveryPointViewSet
)


router = DefaultRouter()
router.register('customers', CustomerViewSet)
router.register('orders', OrderViewSet)
router.register('delivery-points/areas', AreaViewSet)
router.register('delivery-points/streets', StreetViewSet)
router.register('delivery-points', DeliveryPointViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
