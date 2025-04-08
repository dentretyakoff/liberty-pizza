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


class CartItem(BaseModel):
    cart = models.ForeignKey(
        Cart,
        verbose_name='Козина клиента',
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        verbose_name='Товар',
        on_delete=models.CASCADE
    )
    quantity = models.PositiveSmallIntegerField(
        'Количество',
        default=1
    )

    class Meta:
        verbose_name = 'Товар корзины'
        verbose_name_plural = 'Товары корзин'

    def __str__(self):
        return self.product
