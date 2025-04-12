import base64

from rest_framework import serializers

from products.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description')


class ProductListSerializer(serializers.ModelSerializer):
    quantity = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'description',
            'price',
            'category',
            'quantity',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        self.customer = None
        self.telegram_id = request.query_params.get('telegram_id')
        if self.telegram_id:
            from users.models import Customer
            try:
                self.customer = (
                    Customer.objects.select_related('cart')
                    .prefetch_related('cart__items')
                    .get(telegram_id=self.telegram_id))
            except Customer.DoesNotExist:
                self.customer = None

    def get_quantity(self, obj):
        if self.customer:
            cartitem = self.customer.cart.items.filter(product=obj).first()
            return getattr(cartitem, 'quantity', 0)
        return None


class ProductSerializer(ProductListSerializer):
    cartitem_id = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    image_base64 = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'description',
            'price',
            'category',
            'cartitem_id',
            'quantity',
            'total_price',
            'image_base64'
        )

    def get_total_price(self, obj):
        if self.customer:
            return self.customer.cart.total_price
        return None

    def get_cartitem_id(self, obj):
        if self.customer:
            cartitem = self.customer.cart.items.filter(product=obj).first()
            return getattr(cartitem, 'id', None)
        return None

    def get_image_base64(self, obj):
        if obj.image:
            with open(obj.image.path, 'rb') as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        return None
