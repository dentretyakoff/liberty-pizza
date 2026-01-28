from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.methods import SendMessage

from api.users import create_customer, create_cart, get_gdpr, update_customer
from core.constants import MessagesConstants
from handlers.keyboards import (
    main_menu_keyboard,
    back_to_main_keyboard,
    gdpr_confirm_keyboard
)


router = Router()


@router.message(CommandStart())
async def start_handler(message: Message) -> SendMessage:
    """Приветствуем пользователя."""
    hello_message = MessagesConstants.HELLO
    customer = await create_customer(
        message.from_user.id, message.from_user.username)
    await create_cart(message.from_user.id)
    if not customer.get('gdpr_accepted'):
        gdpr = await get_gdpr() or MessagesConstants.DEFAULT_GDPR
        await message.answer(
            text=gdpr,
            reply_markup=gdpr_confirm_keyboard
        )
        return
    await message.answer(
        text=hello_message, reply_markup=main_menu_keyboard)


@router.callback_query(F.data == 'gdpr_confirm')
async def gdpr_confirm(callback_query: CallbackQuery) -> SendMessage:
    """Сохраняет согласие на обработку персональных данных."""
    await update_customer(callback_query.from_user.id, {'gdpr_accepted': True})
    await callback_query.message.edit_text(
        text=MessagesConstants.HELLO,
        reply_markup=main_menu_keyboard)


@router.callback_query(F.data == 'back')
async def back_to_main(callback_query: CallbackQuery) -> SendMessage:
    """Вернуться в главное меню."""
    hello_message = MessagesConstants.HELLO
    await callback_query.message.edit_text(
        text=hello_message,
        reply_markup=main_menu_keyboard)


@router.message(F.text.startswith('/'))
async def unknown_command_handler(message: Message) -> SendMessage:
    """Обработка неизвестной команды."""
    await message.answer(
        text=MessagesConstants.UNKNOWN_COMMAND,
        reply_markup=back_to_main_keyboard)
