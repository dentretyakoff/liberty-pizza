from aiogram.fsm.state import StatesGroup, State


class CartForm(StatesGroup):
    comment = State()
