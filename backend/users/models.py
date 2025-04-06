from django.db import models
from django.core.validators import RegexValidator

from base.models import BaseModel


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
