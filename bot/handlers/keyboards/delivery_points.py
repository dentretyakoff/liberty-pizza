from aiogram.types import InlineKeyboardButton

from handlers.keyboards.base import get_form_keyboard


def generate_areas_buttons(areas: list):
    """Генерирует кнопки выбора зоны доставки."""
    buttons = [
        InlineKeyboardButton(
            text=area.get('name'),
            callback_data=f'area_id_{area.get("id")}')
        for area in areas
    ]
    buttons.append(back_to_cart)
    return get_form_keyboard(*buttons)


def generate_streets_buttons(streets: list):
    """Генерирует кнопки выбора улицы."""
    buttons = [
        InlineKeyboardButton(
            text=f'{street.get("name")} {street.get("cost")} руб.',
            callback_data=f'street_id_{street.get("id")}')
        for street in streets
    ]
    buttons.append(back_to_areas_button)
    return get_form_keyboard(*buttons)


back_to_areas_button = InlineKeyboardButton(
    text='⬅️ Назад к списку зон',
    callback_data='areas'
)
back_to_cart = InlineKeyboardButton(
    text='⬅️ Назад',
    callback_data='cart'
)
