from urllib.parse import urlparse, parse_qs

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.settings import PAGE_SIZE


def get_form_keyboard(
        *buttons,
        one_row_buttons: list[InlineKeyboardButton] = None,
        back_button: list[InlineKeyboardButton] = None):
    builder = InlineKeyboardBuilder()
    for button in buttons:
        builder.add(button)
    builder.adjust(1)
    if one_row_buttons:
        builder.row(*one_row_buttons)
    if back_button:
        builder.row(back_button)

    return builder.as_markup()


def extract_limit_offset(url: str) -> tuple[int, int]:
    if not url:
        return PAGE_SIZE, 0

    parsed = urlparse(url)
    query_dict = parse_qs(parsed.query)

    limit = int(query_dict.get('limit', [PAGE_SIZE])[0])
    offset = int(query_dict.get('offset', [0])[0])

    return limit, offset


def get_pagination_buttons(prefix: str, next_url: str, prev_url: str) -> list:
    buttons = []

    if prev_url:
        limit, offset = extract_limit_offset(prev_url)
        buttons.append(InlineKeyboardButton(
            text='⬅️ Назад',
            callback_data=f'{prefix}_{limit}_{offset}'
        ))

    if next_url:
        limit, offset = extract_limit_offset(next_url)
        buttons.append(InlineKeyboardButton(
            text='Вперёд ➡️',
            callback_data=f'{prefix}_{limit}_{offset}'
        ))

    return buttons


back_to_main_button = InlineKeyboardButton(
    text='🏠 На главную',
    callback_data='back'
)

back_to_main_keyboard = get_form_keyboard(back_to_main_button)
