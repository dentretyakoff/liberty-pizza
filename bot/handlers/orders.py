from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.methods import SendMessage

from handlers.keyboards.base import back_to_main_keyboard

router = Router()


@router.callback_query(F.data == 'orders')
async def orders(callback_query: CallbackQuery) -> SendMessage:
    """Список заказов."""
    return await callback_query.message.edit_text(
        text='Тут будут заказы',
        reply_markup=back_to_main_keyboard)
