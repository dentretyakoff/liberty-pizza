from typing import Any
from datetime import timedelta
from decimal import Decimal, ROUND_DOWN

from django.db import models
from django.conf import settings
from django.utils import timezone

from base.models import BaseModel
from base.enum import PaymentMethod
from users.models import Customer
from products.models import Product
from .enum import OrderStatus


class Order(BaseModel):
    status = models.CharField(
        'Статус оплаты',
        choices=OrderStatus,
        max_length=10,
        blank=True,
        null=True
    )
    customer = models.ForeignKey(
        Customer,
        verbose_name='Клиент',
        related_name='orders',
        on_delete=models.PROTECT
    )
    payment_method = models.CharField(
        'Способ оплаты',
        choices=PaymentMethod,
        default=PaymentMethod.CARD,
        max_length=10
    )
    comment = models.TextField(
        'Комментарий для заказа',
        blank=True,
        default=''
    )
    expiration_date = models.DateTimeField(
        'Срок оплаты',
        null=True,
        blank=True
    )
    payment_url = models.URLField(
        'Ссылка на оплату',
        null=True,
        blank=True,
        max_length=2000
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ № {self.pk}'

    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.pk and self.payment_method == PaymentMethod.ROBOKASSA:
            self.expiration_date = timezone.now() + timedelta(
                seconds=settings.ORDER_MAX_LIFE_TIME
            )
        return super().save(*args, **kwargs)

    def payment_method_display(self):
        return dict(PaymentMethod.choices).get(self.payment_method)

    @property
    def total_price(self) -> Decimal:
        total = sum(
            (item.price * item.quantity for item in self.items.all()),
            start=Decimal('0')
        )
        return str(total.quantize(Decimal('0.01'), rounding=ROUND_DOWN))


class OrderItem(BaseModel):
    order = models.ForeignKey(
        Order,
        verbose_name='Заказ',
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        verbose_name='Товар',
        on_delete=models.CASCADE,
        related_name='orderitems'
    )
    quantity = models.PositiveSmallIntegerField(
        'Количество',
        default=1
    )
    price = models.DecimalField(
        'Цена',
        help_text='Фиксируется в момент добалвения в корзину',
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        verbose_name = 'Товар заказа'
        verbose_name_plural = 'Товары заказов'

    def __str__(self):
        return f'{self.product}'
