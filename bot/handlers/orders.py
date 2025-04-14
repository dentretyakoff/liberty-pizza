from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.methods import SendMessage

from api.orders import create_order
from handlers.keyboards import (
    back_to_main_keyboard,
    create_order_keyboard,
    generate_payment_link_buttons
)
from handlers.utils import get_order_detail

router = Router()


@router.callback_query(F.data == 'orders')
async def orders(callback_query: CallbackQuery) -> SendMessage:
    """Список заказов."""
    await callback_query.message.edit_text(
        text='Тут будут заказы',
        reply_markup=back_to_main_keyboard)


@router.callback_query(F.data == 'order_detail')
async def order_detail(callback_query: CallbackQuery) -> SendMessage:
    """Получает детали заказа."""
    order_detail = await get_order_detail(callback_query.from_user.id)
    await callback_query.message.edit_text(
        text=order_detail,
        reply_markup=create_order_keyboard
    )


@router.callback_query(F.data == 'create_order')
async def make_order(callback_query: CallbackQuery) -> SendMessage:
    """Создает заказ."""
    order = await create_order(callback_query.from_user.id)
    await callback_query.message.edit_text(
        text='Спасибо за заказ.',
        reply_markup=generate_payment_link_buttons(order.get('payment_url')))
