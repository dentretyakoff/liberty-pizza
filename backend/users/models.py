from decimal import Decimal, ROUND_DOWN

from django.db import models
from django.core.validators import RegexValidator

from base.models import BaseModel
from base.enum import PaymentMethod
from products.models import Product


class Customer(BaseModel):
    telegram_id = models.PositiveBigIntegerField(
        'Телеграм ID',
        unique=True
    )
    nickname = models.CharField(
        'Никнейм',
        null=True,
        blank=True,
        max_length=255
    )
    gdpr_accepted = models.BooleanField(
        default=False,
        verbose_name='Согласие на ПД',
        help_text='Статус согласия на обработку перс. данных'
    )
    phone = models.CharField(
        validators=[
            RegexValidator(
                regex=r'^(?:\+7|8)\d{10}$',
                message='Введите номер в формате +71234567890 или 89123456789'
            )
        ],
        max_length=12,
        blank=True
    )

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'{self.telegram_id}'


class Cart(BaseModel):
    customer = models.OneToOneField(
        Customer,
        verbose_name='Клиент',
        on_delete=models.CASCADE,
        related_name='cart'
    )
    payment_method = models.CharField(
        'Способ оплаты',
        choices=PaymentMethod,
        null=True,
        blank=True,
        max_length=10
    )
    comment = models.TextField(
        'Комментарий для заказа',
        blank=True,
        default=''
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f'{self.customer}'

    def payment_method_display(self):
        return dict(PaymentMethod.choices).get(self.payment_method)

    @property
    def total_price(self) -> Decimal:
        total = sum(
            (item.price * item.quantity for item in self.items.all()),
            start=Decimal('0')
        )
        return str(total.quantize(Decimal('0.01'), rounding=ROUND_DOWN))

    @property
    def delivery_price(self) -> str:
        delivery_point = self.customer.delivery_points.filter(
            actual=True).first()
        if delivery_point:
            cost = delivery_point.street.cost
            return str(cost.quantize(Decimal('0.01'), rounding=ROUND_DOWN))
        return '0'

    @property
    def delivery_point(self) -> models.Model:
        delivery_point = self.customer.delivery_points.filter(
            actual=True).first()
        return delivery_point


class CartItem(BaseModel):
    cart = models.ForeignKey(
        Cart,
        verbose_name='Клиент',
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        verbose_name='Товар',
        on_delete=models.CASCADE,
        related_name='cartitems'
    )
    quantity = models.PositiveSmallIntegerField(
        'Количество',
        default=1
    )
    price = models.DecimalField(
        'Цена',
        help_text='Фиксируется в момент добавления в корзину',
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        verbose_name = 'Товар корзины'
        verbose_name_plural = 'Товары корзин'

    def __str__(self):
        return f'{self.product}'


class GDPR(BaseModel):
    name = models.CharField(
        max_length=200,
        verbose_name='Наименование'
    )
    text = models.TextField(
        max_length=2500,
        verbose_name='Текст',
    )
    is_actual = models.BooleanField(
        default=False,
        verbose_name='Актуально'
    )

    class Meta:
        verbose_name = 'Согласие на обработку ПД'
        verbose_name_plural = 'Согласия на обработку ПД'

    def __str__(self):
        return self.name
