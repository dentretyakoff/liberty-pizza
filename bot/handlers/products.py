from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.methods import SendMessage

from api.products import (
    get_categories,
    get_products,
    get_product
)
from api.users import delete_cartitem, add_cartitem
from handlers.keyboards import (
    generate_categories_buttons,
    generate_products_buttons,
    generate_product_buttons
)
from handlers.states import ProductForm
from core.validators import validate_quantity_is_number
from .utils import get_product_detail, make_image_from_base64

router = Router()


@router.callback_query(F.data == 'categories')
async def categories(callback_query: CallbackQuery) -> SendMessage:
    """Список категорий товраов."""
    categories_data = await get_categories()
    await callback_query.message.edit_text(
        text='Выбери категорию товаров:',
        reply_markup=generate_categories_buttons(categories_data))


@router.callback_query(F.data.startswith('category_id_'))
async def products(callback_query: CallbackQuery) -> SendMessage:
    """Список товаров в выбранной категории."""
    category_id = int(callback_query.data.split('_')[-1])
    products_data = await get_products(
        category_id, callback_query.from_user.id)
    await callback_query.message.delete()
    await callback_query.message.answer(
        text='Выбери товар:',
        reply_markup=generate_products_buttons(products_data))


@router.callback_query(F.data.startswith('product_id_'))
async def product(callback_query: CallbackQuery) -> SendMessage:
    """Детальная информация о товаре."""
    product_id = int(callback_query.data.split('_')[-1])
    await answer_with_detail_product(
        product_id=product_id,
        telegram_id=callback_query.from_user.id,
        message=callback_query.message
    )


@router.callback_query(F.data.startswith('delete_cartitem_id_'))
async def delete_cartitem_from_cart(
        callback_query: CallbackQuery) -> SendMessage:
    """Удалаяет товар из корзины."""
    parts = callback_query.data.split('_')
    cartitem_id = int(parts[3])
    product_id = int(parts[4])
    await delete_cartitem(cartitem_id)
    await answer_with_detail_product(
        product_id=product_id,
        telegram_id=callback_query.from_user.id,
        message=callback_query.message
    )


@router.callback_query(F.data.startswith('add_product_id_'))
async def add_cartitem_to_cart(
        callback_query: CallbackQuery,
        state: FSMContext) -> SendMessage:
    """Запоминает выбранный товар."""
    product_id = int(callback_query.data.split('_')[-1])
    await state.update_data(product=product_id)
    await callback_query.message.delete()
    await callback_query.message.answer('Введите количество товара:')
    await state.set_state(ProductForm.quantity)


@router.message(ProductForm.quantity)
async def input_quantity(
        message: Message,
        state: FSMContext) -> SendMessage:
    """Запоминает количество, добавляет товар в корзину."""
    quantity = validate_quantity_is_number(message.text.strip())
    await state.update_data(quantity=quantity)
    data = await state.get_data()
    data['telegram_id'] = message.from_user.id
    await add_cartitem(data)
    await state.clear()
    await answer_with_detail_product(
        product_id=data.get('product'),
        telegram_id=message.from_user.id,
        message=message
    )


async def answer_with_detail_product(
        product_id: int,
        telegram_id: int,
        message: Message | CallbackQuery,
) -> None:
    """Ответ с деталями о товаре."""
    product_data = await get_product(product_id, telegram_id)
    product_detail = await get_product_detail(product_data)
    image_base64 = product_data.get('image_base64')
    await message.delete()
    if image_base64:
        image = await make_image_from_base64(image_base64, 'product')
        return await message.answer_photo(
            photo=image,
            caption=product_detail,
            reply_markup=generate_product_buttons(product_data))
    await message.answer(
        text=product_detail,
        reply_markup=generate_product_buttons(product_data)
    )
