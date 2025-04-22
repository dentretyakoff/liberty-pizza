import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.methods import SendMessage

from api.users import update_customer, update_cart
from handlers.keyboards import (
    create_order_keyboard,
    payment_method_keyboard,
    request_comment_keyboard
)
from handlers.states import UserForm, CartForm
from core.validators import validate_phone_number, validate_message_is_text
from handlers.utils import get_pre_order_detail, delete_previous_message

router = Router()

logger = logging.getLogger(__name__)


@router.callback_query(F.data == 'new_phone')
async def new_phone(
        callback_query: CallbackQuery,
        state: FSMContext) -> SendMessage:
    """Ожидает ввода номера телефона."""
    sent_message = await callback_query.message.edit_text(
        'Введи номер телефона:')
    await state.update_data(phone_message_id=sent_message.message_id)
    await state.set_state(UserForm.phone)


@router.callback_query(F.data == 'exist_phone')
async def exist_phone(
        callback_query: CallbackQuery,
        state: FSMContext) -> SendMessage:
    """При воборе текущего номер телефона переводит на ввод комментария."""
    await state.clear()
    await callback_query.message.edit_text(
        text='Хотел бы оставить комментарий к заказу?',
        reply_markup=request_comment_keyboard
    )


@router.message(UserForm.phone)
async def input_phone(
        message: Message,
        state: FSMContext) -> SendMessage:
    """Запоминает номер телефона клиента."""
    phone = validate_phone_number(message.text.strip())
    await state.update_data(phone=phone)
    data = await state.get_data()
    await update_customer(
        telegram_id=message.from_user.id,
        data={'phone': data.get('phone')})
    await state.clear()
    await delete_previous_message(data.get('phone_message_id'), message)
    await message.answer(
        text='Хотел бы оставить комментарий к заказу?',
        reply_markup=request_comment_keyboard
    )


@router.callback_query(F.data.startswith('request_comment_'))
async def request_comment(
        callback_query: CallbackQuery,
        state: FSMContext) -> SendMessage:
    """Обрабатывает выбор оставления комментария."""
    answer = callback_query.data.split('_')[-1]
    if answer == 'yes':
        sent_message = await callback_query.message.edit_text(
            'Введи текст комментария:')
        await state.update_data(comment_message_id=sent_message.message_id)
        await state.set_state(CartForm.comment)
    else:
        await callback_query.message.edit_text(
            text='Выбери спобоб оплаты:',
            reply_markup=payment_method_keyboard)


@router.message(CartForm.comment)
async def input_comment(
        message: Message,
        state: FSMContext) -> SendMessage:
    """Запоминает комментарий к заказу."""
    comment = validate_message_is_text(message)
    await state.update_data(comment=comment)
    data = await state.get_data()
    await update_cart(
        telegram_id=message.from_user.id,
        data={'comment': data.get('comment')})
    await state.clear()
    await delete_previous_message(data.get('comment_message_id'), message)
    await message.answer(
        text='Выбери спобоб оплаты:',
        reply_markup=payment_method_keyboard)


@router.callback_query(F.data.startswith('payment_'))
async def select_payment_method(callback_query: CallbackQuery) -> SendMessage:
    """Запоминает способ оплаты клиента."""
    payment_method = callback_query.data.split('_')[-1]
    await update_cart(
        telegram_id=callback_query.from_user.id,
        data={'payment_method': payment_method})
    order_detail = await get_pre_order_detail(callback_query.from_user.id)
    await callback_query.message.edit_text(
        text=order_detail,
        reply_markup=create_order_keyboard
    )
