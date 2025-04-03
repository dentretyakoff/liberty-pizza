"""Модуль исключений при валидации."""
from core.exceptions.base import BotError


class ValidationError(BotError):
    """Базовый класс для исключений при валидации."""


class ValidationNoPaymentOrder(ValidationError):
    """Если уже есть неоплаченный заказ."""
    def __init__(self, message: str, response: dict):
        super().__init__(message)
        self.response = response
