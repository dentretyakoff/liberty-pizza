from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_form_keyboard(*buttons):
    builder = InlineKeyboardBuilder()
    for button in buttons:
        builder.add(button)
    builder.adjust(1)
    return builder.as_markup()


back_to_main_button = InlineKeyboardButton(
    text='🏠 На главную',
    callback_data='back'
)

back_to_main_keyboard = get_form_keyboard(back_to_main_button)
