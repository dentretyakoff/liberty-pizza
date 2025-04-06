from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.methods import SendMessage

from api.delivery_points import get_areas, get_streets, create_delivery_point
from api.users import get_customer
from handlers.keyboards import (
    generate_areas_buttons,
    generate_streets_buttons,
    generate_phone_buttons
)
from handlers.states import AddressForm, UserForm
from core.validators import validate_house_number

router = Router()


@router.callback_query(F.data == 'areas')
async def areas(callback_query: CallbackQuery) -> SendMessage:
    """Список зон доставки."""
    areas = await get_areas()
    await callback_query.message.edit_text(
        text='Выбери зону доставки',
        reply_markup=generate_areas_buttons(areas))


@router.callback_query(F.data.startswith('area_id_'))
async def streets(callback_query: CallbackQuery) -> SendMessage:
    """Список улиц."""
    area_id = int(callback_query.data.split('_')[-1])
    streets = await get_streets(area_id)
    await callback_query.message.edit_text(
        text='Выбери улицу',
        reply_markup=generate_streets_buttons(streets))


@router.callback_query(F.data.startswith('street_id_'))
async def street_selected(
        callback_query: CallbackQuery,
        state: FSMContext) -> SendMessage:
    """Запоминает выбранную улицу, просит указать номер дома."""
    street_id = int(callback_query.data.split('_')[-1])
    await state.update_data(street=street_id)
    await callback_query.message.edit_text('Введите номер дома:')
    await state.set_state(AddressForm.house_number)


@router.message(AddressForm.house_number)
async def input_house_number(
        message: Message,
        state: FSMContext) -> SendMessage:
    """Запоминает номер дома."""
    house_number = validate_house_number(message.text.strip())
    await state.update_data(house_number=house_number)
    await message.answer('Введите номер подъезда:')
    await state.set_state(AddressForm.entrance_number)


@router.message(AddressForm.entrance_number)
async def input_entrance_number(
        message: Message,
        state: FSMContext) -> SendMessage:
    """Запоминает номер подъезда."""
    entrance_number = validate_house_number(message.text.strip())
    await state.update_data(entrance_number=entrance_number)
    data = await state.get_data()
    data['telegram_id'] = message.from_user.id
    await create_delivery_point(data)
    await state.clear()
    customer = await get_customer(message.from_user.id)
    phone = customer.get('phone')
    if phone:
        return await message.answer(
            text='Номер телефона для связи',
            reply_markup=generate_phone_buttons(phone))
    await message.answer('Введите номер телефона:')
    await state.set_state(UserForm.phone)
