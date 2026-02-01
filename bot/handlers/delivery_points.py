from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.methods import SendMessage

from api.delivery_points import (
    get_areas,
    get_streets,
    get_street,
    create_delivery_point,
    get_my_delivery_points,
    set_my_delivery_point
)
from api.users import get_customer, update_cart
from handlers.keyboards import (
    generate_areas_buttons,
    generate_streets_buttons,
    generate_phone_buttons,
    generate_my_delivery_points_buttons
)
from handlers.states import AddressForm, UserForm
from core.validators import validate_house_number
from core.constants import ReceiptMethods
from .utils import delete_previous_message, ask_or_show_phone

router = Router()


@router.callback_query(F.data == 'areas')
async def areas(callback_query: CallbackQuery) -> SendMessage:
    """Список зон доставки."""
    data = await get_areas()
    areas = data.get('results')
    await callback_query.message.edit_text(
        text='Выбери зону доставки',
        reply_markup=generate_areas_buttons(areas))


@router.callback_query(F.data.startswith('area_id_'))
async def streets(callback_query: CallbackQuery) -> SendMessage:
    """Список улиц."""
    parts = callback_query.data.split('_')
    area_id = int(parts[2])
    limit = int(parts[3])
    offset = int(parts[4])
    data = await get_streets(area_id, limit, offset)
    await callback_query.message.edit_text(
        text='Выбери улицу',
        reply_markup=generate_streets_buttons(data, f'area_id_{area_id}'))


@router.callback_query(F.data.startswith('street_id_'))
async def street_selected(
        callback_query: CallbackQuery,
        state: FSMContext) -> SendMessage:
    """Запоминает выбранную улицу, просит указать номер дома."""
    street_id = int(callback_query.data.split('_')[-1])
    await state.update_data(street=street_id)
    sent_message = await callback_query.message.edit_text(
        'Введите номер дома:')
    await state.update_data(message_id=sent_message.message_id)
    await state.set_state(AddressForm.house_number)


@router.message(AddressForm.house_number)
async def input_house_number(
        message: Message,
        state: FSMContext) -> SendMessage:
    """Запоминает номер дома."""
    house_number = validate_house_number(message.text.strip())
    await state.update_data(house_number=house_number)
    data = await state.get_data()
    await delete_previous_message(data.pop('message_id'), message)
    street = await get_street(data.get('street'))
    exists_entrance = street.get('exists_entrance')
    if exists_entrance:
        sent_message = await message.answer('Введите номер подъезда:')
        await state.update_data(message_id=sent_message.message_id)
        await state.set_state(AddressForm.entrance_number)
    else:
        data['telegram_id'] = message.from_user.id
        await create_delivery_point(data)
        await state.clear()
        customer = await get_customer(message.from_user.id)
        phone = customer.get('phone')
        if phone:
            return await message.answer(
                text='Номер телефона для связи',
                reply_markup=generate_phone_buttons(phone))
        sent_message = await message.answer('Введите номер телефона:')
        await state.update_data(phone_message_id=sent_message.message_id)
        await state.set_state(UserForm.phone)


@router.message(AddressForm.entrance_number)
async def input_entrance_number(
        message: Message,
        state: FSMContext) -> SendMessage:
    """Запоминает номер подъезда."""
    entrance_number = validate_house_number(message.text.strip())
    await state.update_data(entrance_number=entrance_number)
    data = await state.get_data()
    data['telegram_id'] = message.from_user.id
    await delete_previous_message(data.pop('message_id'), message)
    await create_delivery_point(data)
    await state.clear()
    customer = await get_customer(message.from_user.id)
    phone = customer.get('phone')
    if phone:
        return await message.answer(
            text='Номер телефона для связи',
            reply_markup=generate_phone_buttons(phone))
    sent_message = await message.answer('Введите номер телефона:')
    await state.update_data(phone_message_id=sent_message.message_id)
    await state.set_state(UserForm.phone)


@router.callback_query(F.data == 'my_delivery_points')
async def my_delivery_points(callback_query: CallbackQuery) -> SendMessage:
    """Список точек доставки клиента."""
    data = await get_my_delivery_points(callback_query.from_user.id)
    delivery_points = data.get('results')
    await callback_query.message.edit_text(
        text='Выбери точку доставки',
        reply_markup=generate_my_delivery_points_buttons(delivery_points))


@router.callback_query(F.data.startswith('delivery_point_id'))
async def set_delivery_point(
        callback_query: CallbackQuery,
        state: FSMContext) -> SendMessage:
    """Запоминает выбранную точку доставки клиента."""
    delivery_point_id = int(callback_query.data.split('_')[-1])
    await set_my_delivery_point(delivery_point_id)
    await update_cart(
        callback_query.from_user.id,
        {'receipt_method_type': ReceiptMethods.DELIVERY})
    await ask_or_show_phone(callback_query, state)
