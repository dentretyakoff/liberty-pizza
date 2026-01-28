from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .orders.views import OrderViewSet
from .users.views import (
    CustomerViewSet,
    CartViewSet,
    CartItemViewSet,
    GDPRViewSet
)
from .delivery_points.views import (
    AreaViewSet,
    StreetViewSet,
    DeliveryPointViewSet
)
from .products.views import CategoryViewSet, ProductViewSet
from .about.views import ContactViewSet


router = DefaultRouter()
router.register('customers/cart', CartViewSet)
router.register('customers/cart-items', CartItemViewSet)
router.register('customers', CustomerViewSet)
router.register('orders', OrderViewSet)
router.register('delivery-points/areas', AreaViewSet)
router.register('delivery-points/streets', StreetViewSet)
router.register('delivery-points', DeliveryPointViewSet)
router.register('categories', CategoryViewSet)
router.register('products', ProductViewSet)
router.register('contacts', ContactViewSet)
router.register('gdpr', GDPRViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
