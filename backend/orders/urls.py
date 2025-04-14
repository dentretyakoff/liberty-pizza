from django.urls import path
from .views import robokassa_redirect


app_name = 'orders'


urlpatterns = [
    path('pay/<int:order_id>/', robokassa_redirect, name='robokassa_redirect'),
]
