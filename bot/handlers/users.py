from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.methods import SendMessage

from api.users import update_customer
from handlers.keyboards import create_order_keyboard
from handlers.states import UserForm
from core.validators import validate_phone_number
from handlers.utils import get_order_detail

router = Router()


@router.callback_query(F.data == 'new_phone')
async def new_phone(
        callback_query: CallbackQuery,
        state: FSMContext) -> SendMessage:
    """Ожидает ввода номера телефона."""
    await callback_query.message.edit_text('Введите номер телефона:')
    await state.set_state(UserForm.phone)


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
    order_detail = await get_order_detail(message.from_user.id)
    await message.answer(
        text=order_detail,
        reply_markup=create_order_keyboard
    )
