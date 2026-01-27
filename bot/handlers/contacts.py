import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.methods import SendMessage

from api.about import get_contacts
from handlers.keyboards import back_to_main_keyboard
from .utils import make_message_contacts


router = Router()

logger = logging.getLogger(__name__)


@router.callback_query(F.data == 'contacts')
async def contacts(
        callback_query: CallbackQuery,
        state: FSMContext) -> SendMessage:
    """Контакты магазина."""
    contacts = await get_contacts()
    text = make_message_contacts(contacts)
    await callback_query.message.edit_text(
        text=text,
        reply_markup=back_to_main_keyboard
    )
