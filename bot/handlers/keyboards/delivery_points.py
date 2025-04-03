from aiogram.types import InlineKeyboardButton

from handlers.keyboards.base import get_form_keyboard, back_to_main_button


def generate_areas_buttons(areas: list):
    """Генерирует кнопки выбора зоны доставки."""
    buttons = [
        InlineKeyboardButton(
            text=area.get('name'),
            callback_data=f'area_id_{area.get("id")}')
        for area in areas
    ]
    buttons.append(back_to_main_button)
    return get_form_keyboard(*buttons)


def generate_streets_buttons(streets: list):
    """Генерирует кнопки выбора улицы."""
    buttons = [
        InlineKeyboardButton(
            text=f'{area.get("name")} {area.get("cost")} руб.',
            callback_data=f'area_id_{area.get("id")}')
        for area in streets
    ]
    buttons.append(areas_button)
    return get_form_keyboard(*buttons)


areas_button = InlineKeyboardButton(
    text='⬅️ Назад к списку зон',
    callback_data='areas'
)
