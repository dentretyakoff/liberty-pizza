from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.methods import SendMessage

from api.users import get_cart
from handlers.keyboards import cart_menu
from .utils import get_cart_detail

router = Router()


@router.callback_query(F.data == 'cart')
async def cart(callback_query: CallbackQuery) -> SendMessage:
    """Корзина пользователя."""
    cart = await get_cart(callback_query.from_user.id)
    cart_detail = await get_cart_detail(cart)
    await callback_query.message.delete()
    await callback_query.message.answer(
        text=cart_detail, reply_markup=cart_menu)
