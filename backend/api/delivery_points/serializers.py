from rest_framework import serializers

from delivery_points.models import Street, Area, DeliveryPoint
from users.models import Customer


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


class DeliveryPointCreateSerializer(serializers.ModelSerializer):
    telegram_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = DeliveryPoint
        fields = ('id', 'street', 'house_number', 'telegram_id')

    def create(self, validated_data):
        telegram_id = validated_data.pop('telegram_id')
        try:
            customer = Customer.objects.get(telegram_id=telegram_id)
        except Customer.DoesNotExist:
            raise serializers.ValidationError(
                'Пользователь с таким Telegram ID не найден')

        delivery_point, _ = DeliveryPoint.objects.get_or_create(
            customer=customer,
            street=validated_data.get('street'),
            house_number=validated_data.get('house_number'))
        return delivery_point


class DeliveryPointSerializer(serializers.ModelSerializer):
    customer = serializers.SlugRelatedField(
        read_only=True,
        slug_field='telegram_id'
    )
    street = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = DeliveryPoint
        fields = ('id', 'customer', 'street', 'house_number')
