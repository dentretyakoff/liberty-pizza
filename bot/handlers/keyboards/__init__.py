# flake8: noqa
from handlers.keyboards.delivery_points import (
    generate_areas_buttons,
    generate_streets_buttons,
    generate_my_delivery_points_buttons
)
from handlers.keyboards.users import (
    generate_phone_buttons,
    payment_method_keyboard
)
from handlers.keyboards.base import back_to_main_keyboard
from handlers.keyboards.cart import cart_menu, areas_button
from handlers.keyboards.common import main_menu_keyboard
from handlers.keyboards.orders import create_order_keyboard