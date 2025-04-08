from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response

from users.models import Customer, Cart
from .serializers import (
    CustomerCreateSerializer,
    CustomerUpdateSerializer,
    CustomerRetrieveSerializer,
    CartCreateSerializer,
    CartUpdateSerializer,
    CartRetrieveSerializer
)


class CustomerViewSet(mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    queryset = Customer.objects.all()
    lookup_field = 'telegram_id'
    serializer_class = CustomerCreateSerializer

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return CustomerUpdateSerializer
        elif self.action in ['retrieve', 'list']:
            return CustomerRetrieveSerializer
        return CustomerCreateSerializer


class CartViewSet(mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartCreateSerializer

    def get_object(self):
        telegram_id = self.kwargs.get('pk')
        customer = get_object_or_404(Customer, telegram_id=telegram_id)
        return Cart.objects.get(customer=customer)

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return CartUpdateSerializer
        elif self.action == 'retrieve':
            return CartRetrieveSerializer
        return CartCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        detail_serializer = CartRetrieveSerializer(
            serializer.instance,
            context=self.get_serializer_context())
        headers = self.get_success_headers(detail_serializer.data)
        return Response(
            detail_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers)
