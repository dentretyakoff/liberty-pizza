from rest_framework import serializers

from api.delivery_points.serializers import DeliveryPointSerializer
from users.models import Customer, Cart, CartItem, GDPR


class CustomerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('telegram_id', 'nickname', 'gdpr_accepted')


class CustomerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('nickname', 'phone', 'gdpr_accepted')


class CustomerRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'telegram_id', 'nickname', 'phone', 'gdpr_accepted')


class CartCreateSerializer(serializers.ModelSerializer):
    telegram_id = serializers.CharField(write_only=True)

    class Meta:
        model = Cart
        fields = ('telegram_id',)

    def validate(self, data):
        telegram_id = data.pop('telegram_id', None)
        try:
            customer = Customer.objects.get(telegram_id=telegram_id)
        except Customer.DoesNotExist:
            raise serializers.ValidationError(
                'Пользователь с таким Telegram ID не найден.')
        data['customer'] = customer
        return data

    def create(self, validated_data):
        cart, _ = Cart.objects.get_or_create(
            customer=validated_data.get('customer')
        )
        return cart


class CartUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('payment_method', 'comment', 'receipt_method_type')


class CartItemRetrieveSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source='product.name', read_only=True)

    class Meta:
        model = CartItem
        fields = (
            'id',
            'cart',
            'product',
            'product_name',
            'quantity',
            'price')


class CartRetrieveSerializer(serializers.ModelSerializer):
    customer = CustomerRetrieveSerializer()
    delivery_point = DeliveryPointSerializer()
    items = CartItemRetrieveSerializer(many=True, read_only=True)
    type = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = (
            'id',
            'customer',
            'type',
            'payment_method',
            'payment_method_display',
            'comment',
            'receipt_method_type',
            'total_price',
            'delivery_price',
            'delivery_point',
            'items',
        )

    def get_payment_method_display(self, obj):
        return obj.get_payment_method_display()

    def get_type(self, obj):
        return 'cart'


class CartItemCreateSerializer(serializers.ModelSerializer):
    telegram_id = serializers.CharField(write_only=True)

    class Meta:
        model = CartItem
        fields = ('id', 'telegram_id', 'product', 'quantity')

    def validate(self, data):
        telegram_id = data.pop('telegram_id', None)
        try:
            customer = Customer.objects.get(telegram_id=telegram_id)
        except Customer.DoesNotExist:
            raise serializers.ValidationError(
                'Пользователь с таким Telegram ID не найден.')
        data['cart'] = customer.cart
        return data

    def create(self, validated_data):
        product = validated_data['product']
        validated_data['price'] = product.price
        return super().create(validated_data)


class GDPRSerializer(serializers.ModelSerializer):
    class Meta:
        model = GDPR
        fields = (
            'id',
            'name',
            'text',
            'is_actual'
        )
