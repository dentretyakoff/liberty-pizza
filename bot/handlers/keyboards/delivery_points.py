from aiogram.types import InlineKeyboardButton

from core.settings import PAGE_SIZE
from handlers.keyboards.base import get_form_keyboard, get_pagination_buttons
from handlers.keyboards.cart import areas_button


def generate_areas_buttons(areas: list):
    """Генерирует кнопки выбора зоны доставки."""
    buttons = [
        InlineKeyboardButton(
            text=area.get('name'),
            callback_data=f'area_id_{area.get("id")}_{PAGE_SIZE}_0')
        for area in areas
    ]
    buttons.append(back_to_cart)
    return get_form_keyboard(*buttons)


def generate_streets_buttons(data: dict, prefix: str):
    """Генерирует кнопки выбора улицы."""
    streets = data.get('results')
    buttons = [
        InlineKeyboardButton(
            text=f'{street.get("name")} - {street.get("cost")} руб.',
            callback_data=f'street_id_{street.get("id")}')
        for street in streets
    ]
    pagination_buttons = get_pagination_buttons(
        prefix=prefix,
        next_url=data.get('next'),
        prev_url=data.get('previous')
    )
    return get_form_keyboard(
        *buttons,
        one_row_buttons=pagination_buttons,
        back_button=back_to_areas_button
    )


def generate_my_delivery_points_buttons(delivery_points: dict):
    """Генерирует кнопки выбора точки доставки."""
    buttons = []
    for dp in delivery_points:
        text = f'{dp.get("street")}, {dp.get("house_number")}'
        if dp.get('entrance_number'):
            text += f', подъезд {dp.get("entrance_number")}'
        buttons.append(
            InlineKeyboardButton(
                text=text,
                callback_data=f'delivery_point_id_{dp.get("id")}'
            )
        )

    buttons.append(areas_button)
    return get_form_keyboard(*buttons)


back_to_areas_button = InlineKeyboardButton(
    text='⬅️ Назад к списку зон',
    callback_data='areas'
)
back_to_cart = InlineKeyboardButton(
    text='⬅️ Назад',
    callback_data='cart'
)
