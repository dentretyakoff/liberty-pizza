from rest_framework import serializers

from delivery_points.models import Street, Area


class StreetSerializer(serializers.ModelSerializer):
    area = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Street
        fields = ('id', 'name', 'cost', 'area')


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ('id', 'name')
