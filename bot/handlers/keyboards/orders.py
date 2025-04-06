from aiogram.types import InlineKeyboardButton

from handlers.keyboards.base import get_form_keyboard, back_to_main_button


create_order_button = InlineKeyboardButton(
    text='Создать',
    callback_data='create_order'
)

create_order_keyboard = get_form_keyboard(
    create_order_button,
    back_to_main_button
)
