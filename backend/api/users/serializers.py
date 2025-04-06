from rest_framework import serializers

from users.models import Customer


class CustomerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('telegram_id', 'nickname')


class CustomerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('nickname', 'phone')


class CustomerRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'telegram_id', 'nickname', 'phone')
