from typing import Any
from datetime import timedelta

from django.db import models
from django.conf import settings
from django.utils import timezone

from base.models import BaseModel
from users.models import Customer
from .enum import OrderStatus


class Order(BaseModel):
    status = models.CharField(
        'Статус оплаты',
        choices=OrderStatus,
        default=OrderStatus.AWAITING,
        max_length=10
    )
    customer = models.ForeignKey(
        Customer,
        verbose_name='Клиент',
        related_name='orders',
        on_delete=models.PROTECT
    )
    cost = models.DecimalField(
        'Сумма',
        help_text='Используется в ссылке на оплату',
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
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
        if not self.pk:
            self.expiration_date = timezone.now() + timedelta(
                seconds=settings.ORDER_MAX_LIFE_TIME
            )
        return super().save(*args, **kwargs)
