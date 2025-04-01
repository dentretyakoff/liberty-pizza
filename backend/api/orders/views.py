from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from orders.enum import OrderStatus
from orders.models import Order
from payment import robokassa
from .serializers import (
    OrderCreateSerializer,
    OrderRetrieveSerializer,
)


class OrderViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderRetrieveSerializer
        return OrderCreateSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        cost = 1  # TODO
        quantity = 1  # TODO
        receipt = {
            'items': [
                {
                    'name': 'Стикер AUTO VEGAS',
                    'quantity': quantity,
                    'sum': int(cost),
                    'tax': 'none',
                }
            ]
        }
        payment_url = robokassa.generate_payment_link(
            merchant_login=settings.MERCHANT_LOGIN,
            merchant_password_1=settings.MERCHANT_PASSWORD_1,
            cost=cost,
            number=order.pk,
            expiration_date=order.expiration_date,
            receipt=receipt,
            is_test=settings.IS_TEST
        )
        order.payment_url = payment_url
        order.cost = cost
        order.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer = OrderRetrieveSerializer(instance=serializer.instance)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    @action(detail=True, methods=['patch'])
    def cancel_order(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.status = OrderStatus.CANCELLED
        order.save()
        order.reserve_cancel()
        serializer = OrderRetrieveSerializer(instance=order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False,
            methods=['get'],
            permission_classes=[AllowAny],
            url_path='success-payment')
    def success_payment(self, request):
        query_string = request.get_full_path()
        sign = robokassa.result_payment(
            merchant_password_2=settings.MERCHANT_PASSWORD_2,
            request=query_string)
        if 'OK' in sign:
            order_id = request.query_params.get('InvId')
            order = get_object_or_404(Order, pk=order_id)
            order.paid_success()
            return Response(sign, status=status.HTTP_200_OK)
        return Response(sign, status=status.HTTP_400_BAD_REQUEST)
