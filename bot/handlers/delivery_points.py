from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.methods import SendMessage

from handlers.keyboards.delivery_points import (
    generate_areas_buttons,
    generate_streets_buttons
)
from api.delivery_points import get_areas, get_streets

router = Router()


@router.callback_query(F.data == 'areas')
async def areas(callback_query: CallbackQuery) -> SendMessage:
    """Список зон доставки."""
    areas = await get_areas()
    return await callback_query.message.edit_text(
        text='Выбери зону доставки',
        reply_markup=generate_areas_buttons(areas))


@router.callback_query(F.data.startswith('area_id_'))
async def streets(callback_query: CallbackQuery) -> SendMessage:
    """Список улиц."""
    area_id = int(callback_query.data.split('_')[-1])
    streets = await get_streets(area_id)
    return await callback_query.message.edit_text(
        text='Выбери улицу',
        reply_markup=generate_streets_buttons(streets))
