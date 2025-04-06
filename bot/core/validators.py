import re

from core.constants import HOUSE_NUMBER_PATTERN, PHONE_PATTERN
from core.exceptions.validations import ValidationError


def validate_house_number(number: str) -> str:
    """Проверяет номер дома для адреса доставки."""
    if not re.match(HOUSE_NUMBER_PATTERN, number.strip()):
        raise ValidationError(
            'Некорректный номер дома, пожалуйста, попробуйте еще раз.')
    return number.strip()


def validate_phone_number(phone: str) -> str:
    """Проверяет номер телефона клиента."""
    if not re.match(PHONE_PATTERN, phone.strip()):
        raise ValidationError(
            'Некорректный номер телефона.\n'
            'Пожалуйста введите в формате +71234567890 или 89123456789.')
    return phone.strip()
