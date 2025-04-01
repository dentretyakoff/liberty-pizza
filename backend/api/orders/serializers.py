from rest_framework import serializers

from orders.models import Order


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('telegram_user',)


class OrderRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'status', 'payment_url',
                  'telegram_user', 'tickets_count',
                  'expiration_date')
