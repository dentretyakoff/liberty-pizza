from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.methods import SendMessage

from handlers.keyboards import back_to_main_keyboard

router = Router()


@router.callback_query(F.data == 'categoies')
async def categoies(callback_query: CallbackQuery) -> SendMessage:
    """Список категорий товраов."""
    await callback_query.message.edit_text(
        text='Тут будут товары',
        reply_markup=back_to_main_keyboard)
