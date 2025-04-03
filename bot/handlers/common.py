from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.methods import SendMessage

from core.constants import MessagesConstants
from handlers.keyboards.common import main_menu_keyboard
from handlers.keyboards.base import back_to_main_keyboard


router = Router()


@router.message(CommandStart())
async def start_handler(message: Message) -> SendMessage:
    """Приветствуем пользователя."""
    hello_message = MessagesConstants.HELLO
    return await message.answer(
        text=hello_message, reply_markup=main_menu_keyboard)


@router.callback_query(F.data == 'back')
async def back_to_main(callback_query: CallbackQuery) -> SendMessage:
    """Вернуться в главное меню."""
    hello_message = MessagesConstants.HELLO
    return await callback_query.message.edit_text(
        text=hello_message,
        reply_markup=main_menu_keyboard)


@router.message(F.text)
async def unknown_command_handler(message: Message) -> SendMessage:
    """Обработка неизвестной команды."""
    return await message.answer(
        text=MessagesConstants.UNKNOWN_COMMAND,
        reply_markup=back_to_main_keyboard)
