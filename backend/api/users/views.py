from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from users.models import Customer, Cart, CartItem, GDPR
from .serializers import (
    CustomerCreateSerializer,
    CustomerUpdateSerializer,
    CustomerRetrieveSerializer,
    CartCreateSerializer,
    CartUpdateSerializer,
    CartRetrieveSerializer,
    CartItemCreateSerializer,
    CartItemRetrieveSerializer,
    GDPRSerializer
)
from .pagination import LargeLimitOffsetPagination


class CustomerViewSet(mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    queryset = Customer.objects.all()
    lookup_field = 'telegram_id'
    serializer_class = CustomerRetrieveSerializer

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return CustomerUpdateSerializer
        if self.action == 'create':
            return CustomerCreateSerializer
        return CustomerRetrieveSerializer


class CartViewSet(mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = Cart.objects.all().select_related('items')
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

    @action(detail=True, methods=['post'])
    def clear(self, request, pk=None):
        cart = self.get_object()

        cart.items.all().delete()
        cart.comment = ''
        cart.save(update_fields=['comment'])

        serializer = CartRetrieveSerializer(
            cart,
            context=self.get_serializer_context()
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartItemViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemRetrieveSerializer
    pagination_class = LargeLimitOffsetPagination

    def get_queryset(self):
        telegram_id = self.request.query_params.get('telegram_id')
        queryset = CartItem.objects.all().select_related('product')
        if telegram_id:
            queryset = queryset.filter(
                cart__customer__telegram_id=telegram_id)
        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return CartItemCreateSerializer
        return CartItemRetrieveSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        detail_serializer = CartItemRetrieveSerializer(
            serializer.instance,
            context=self.get_serializer_context())
        headers = self.get_success_headers(detail_serializer.data)
        return Response(
            detail_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers)


class GDPRViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = GDPR.objects.filter(is_actual=True)
    serializer_class = GDPRSerializer
