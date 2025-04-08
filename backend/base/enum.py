from django.db import models


class PaymentMethod(models.TextChoices):
    CASH = 'cash', 'Наличные'
    CARD = 'card', 'Карта'
    ROBOKASSA = 'robokassa', 'Робокасса'
