from rest_framework import serializers

from orders.models import Order, OrderItem
from users.models import Customer


class OrderItemRetrieveSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source='product.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = (
            'id',
            'product',
            'product_name',
            'quantity',
            'price'
        )


class OrderCreateSerializer(serializers.ModelSerializer):
    telegram_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Order
        fields = ('telegram_id', 'payment_method')

    def validate_telegram_id(self, value):
        """Проверяем, что клиент с таким telegram_id существует."""
        customer = Customer.objects.filter(telegram_id=value)
        if not customer.exists():
            raise serializers.ValidationError(
                f'Клиент с telegram_id = {value} не найден')
        if not customer.first().cart.items.all().exists():
            raise serializers.ValidationError(
                'Корзина клиента пуста.'
            )
        return value

    def create(self, validated_data):
        telegram_id = validated_data.pop('telegram_id')
        customer = Customer.objects.get(telegram_id=telegram_id)
        cart = customer.cart
        # TODO заполнять status и payment_url если оплата robokassa
        order = Order.objects.create(
            payment_method=cart.payment_method,
            customer=customer,
            comment=cart.comment,
        )
        cart_items = cart.items.all()
        order_items = [
            OrderItem(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.price
            ) for item in cart_items
        ]
        OrderItem.objects.bulk_create(order_items)
        cart.items.all().delete()
        cart.comment = ''
        cart.save()
        return order


class OrderRetrieveSerializer(serializers.ModelSerializer):
    items = OrderItemRetrieveSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = (
            'id',
            'status',
            'customer',
            'payment_method',
            'payment_method_display',
            'comment',
            'total_price',
            'expiration_date',
            'payment_url',
            'items'
        )

    def get_payment_method_display(self, obj):
        return obj.get_payment_method_display()
