import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.methods import SendMessage

from api.users import get_cart, update_cart
from handlers.keyboards import generate_cart_buttons, receipt_method_keyboard
from core.constants import ReceiptMethods
from .utils import get_cart_detail, safe_delete_message, ask_or_show_phone

router = Router()

logger = logging.getLogger(__name__)


@router.callback_query(F.data == 'cart')
async def cart(callback_query: CallbackQuery) -> SendMessage:
    """Корзина пользователя."""
    cart = await get_cart(callback_query.from_user.id)
    cart_detail = await get_cart_detail(cart)
    await safe_delete_message(callback_query.message)
    await callback_query.message.answer(
        text=cart_detail, reply_markup=generate_cart_buttons(cart))


@router.callback_query(F.data == 'receipt_method')
async def receipt_method_order(callback_query: CallbackQuery) -> SendMessage:
    """Способ получения заказа."""
    await callback_query.message.edit_text(
            text='Способ получения',
            reply_markup=receipt_method_keyboard,
        )


@router.callback_query(F.data == 'pickup')
async def pickup(
        callback_query: CallbackQuery,
        state: FSMContext) -> SendMessage:
    await update_cart(
        callback_query.from_user.id,
        {'receipt_method_type': ReceiptMethods.PICKUP})
    await ask_or_show_phone(callback_query, state)
