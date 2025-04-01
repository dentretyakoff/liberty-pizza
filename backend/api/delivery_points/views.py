from rest_framework import mixins, viewsets

from delivery_points.models import Area, Street
from .serializers import AreaSerializer, StreetSerializer


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
