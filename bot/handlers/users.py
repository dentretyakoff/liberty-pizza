from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.methods import SendMessage

from api.users import update_customer, update_cart
from handlers.keyboards import create_order_keyboard, payment_method_keyboard
from handlers.states import UserForm, CartForm
from core.validators import validate_phone_number, validate_message_is_text
from handlers.utils import get_pre_order_detail

router = Router()


@router.callback_query(F.data == 'new_phone')
async def new_phone(
        callback_query: CallbackQuery,
        state: FSMContext) -> SendMessage:
    """Ожидает ввода номера телефона."""
    await callback_query.message.edit_text('Введите номер телефона:')
    await state.set_state(UserForm.phone)


@router.callback_query(F.data == 'exist_phone')
async def exist_phone(
        callback_query: CallbackQuery,
        state: FSMContext) -> SendMessage:
    """При воборе текущего номер телефона переводит на ввод комментария."""
    await callback_query.message.edit_text('Оставь комментарий к заказу:')
    await state.set_state(CartForm.comment)


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
    await message.answer('Оставь комментарий к заказу:')
    await state.set_state(CartForm.comment)


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
