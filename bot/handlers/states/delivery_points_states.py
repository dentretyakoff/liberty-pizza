from aiogram.fsm.state import StatesGroup, State


class AddressForm(StatesGroup):
    street = State()
    house_number = State()
    entrance_number = State()
