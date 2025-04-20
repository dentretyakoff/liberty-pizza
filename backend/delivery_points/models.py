from django.db import models

from base.models import BaseModel
from users.models import Customer


class Street(BaseModel):
    name = models.CharField(
        'Улица',
        max_length=200
    )
    cost = models.DecimalField(
        'Стоимость',
        help_text='Стоимость доставки',
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )
    area = models.ForeignKey(
        'Area',
        verbose_name='Зона доставка',
        related_name='streets',
        on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = 'Улица'
        verbose_name_plural = 'Улицы'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}'


class Area(BaseModel):
    name = models.CharField(
        'Название',
        help_text='Используется для группировки улиц в кнопках',
        max_length=200
    )

    class Meta:
        verbose_name = 'Зона доставки'
        verbose_name_plural = 'Зоны доставки'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}'


class DeliveryPoint(BaseModel):
    customer = models.ForeignKey(
        Customer,
        verbose_name='Клиент',
        related_name='delivery_points',
        on_delete=models.CASCADE
    )
    street = models.ForeignKey(
        Street,
        verbose_name='Улица',
        related_name='delivery_points',
        on_delete=models.PROTECT
    )
    house_number = models.CharField(
        'Номер дома',
        max_length=200
    )
    entrance_number = models.PositiveSmallIntegerField(
        'Номер подъезда',
    )
    actual = models.BooleanField(
        'Текущий',
        default=True
    )

    class Meta:
        verbose_name = 'Точка доставки'
        verbose_name_plural = 'Точки доставки'
        ordering = ('street__name',)

    def __str__(self):
        return f'{self.street.name} {self.house_number}'

    @property
    def street_display(self):
        return f'{self.street.name}'
