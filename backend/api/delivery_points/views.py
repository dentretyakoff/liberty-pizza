from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from delivery_points.models import Area, Street, DeliveryPoint
from users.models import Customer
from .serializers import (
    AreaSerializer,
    StreetSerializer,
    DeliveryPointSerializer,
    DeliveryPointCreateSerializer
)


class StreetViewSet(mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = Street.objects.all()
    serializer_class = StreetSerializer

    def get_queryset(self):
        queryset = Street.objects.all()
        area_id = self.request.query_params.get('area_id')

        if area_id:
            queryset = queryset.filter(area_id=area_id)

        return queryset


class AreaViewSet(mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer


class DeliveryPointViewSet(mixins.CreateModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.ListModelMixin,
                           mixins.UpdateModelMixin,
                           viewsets.GenericViewSet):
    queryset = DeliveryPoint.objects.all()
    serializer_class = DeliveryPointSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return DeliveryPointCreateSerializer
        return DeliveryPointSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        telegram_id = self.request.query_params.get('telegram_id')
        if telegram_id:
            queryset = queryset.filter(customer__telegram_id=telegram_id)
        return queryset

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        customer = instance.customer
        if request.data.get('actual') is True:
            customer.delivery_points.update(actual=False)
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def actual(self, request):
        telegram_id = request.GET.get('telegram_id')
        customer = Customer.objects.filter(
            telegram_id=telegram_id).first()
        delivery_point = customer.delivery_points.filter(actual=True).first()
        serializer = self.get_serializer(delivery_point)
        return Response(serializer.data, status=status.HTTP_200_OK)
