from aiogram.fsm.state import StatesGroup, State


class ProductForm(StatesGroup):
    product = State()
    quantity = State()
    request_msg_id = State()
