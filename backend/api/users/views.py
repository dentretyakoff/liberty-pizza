from rest_framework import mixins, viewsets

from users.models import Customer
from .serializers import (
    CustomerCreateSerializer,
    CustomerUpdateSerializer,
    CustomerRetrieveSerializer,
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
        if self.action == 'update':
            return CustomerUpdateSerializer
        elif self.action in ['retrieve', 'list']:
            return CustomerRetrieveSerializer
        return CustomerCreateSerializer
