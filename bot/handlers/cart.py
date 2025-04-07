from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.methods import SendMessage

from handlers.keyboards import cart_menu

router = Router()


@router.callback_query(F.data == 'cart')
async def cart(callback_query: CallbackQuery) -> SendMessage:
    """Корзина пользователя."""
    await callback_query.message.edit_text(
        text='Тут будет корзина пользователя.',
        reply_markup=cart_menu)
