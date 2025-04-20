from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.methods import SendMessage

from api.orders import create_order, get_orders, get_order
from handlers.keyboards import (
    generate_payment_link_buttons,
    generate_orders_buttons,
    back_to_orders_keyboard
)
from handlers.utils import get_order_detail

router = Router()


@router.callback_query(F.data == 'orders')
async def orders(callback_query: CallbackQuery) -> SendMessage:
    """Список заказов."""
    orders = await get_orders(callback_query.from_user.id)
    text = 'Список заказов:'
    if orders.get('count') == 0:
        text = 'Вы еще не делали заказов.'
    await callback_query.message.edit_text(
        text=text,
        reply_markup=generate_orders_buttons(orders.get('results')))


@router.callback_query(F.data.startswith('order_id_'))
async def order_detail(callback_query: CallbackQuery) -> SendMessage:
    """Детали заказа клиента."""
    order_id = int(callback_query.data.split('_')[-1])
    order = await get_order(order_id)
    text = await get_order_detail(order)
    await callback_query.message.edit_text(
        text=text,
        reply_markup=back_to_orders_keyboard)


@router.callback_query(F.data == 'create_order')
async def make_order(callback_query: CallbackQuery) -> SendMessage:
    """Создает заказ."""
    order = await create_order(callback_query.from_user.id)
    await callback_query.message.edit_text(
        text='Спасибо за заказ.',
        reply_markup=generate_payment_link_buttons(order.get('payment_url')))
