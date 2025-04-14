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
from handlers.keyboards.base import (
    back_to_main_keyboard,
    back_to_main_button,
    get_form_keyboard
)
from handlers.keyboards.cart import areas_button, generate_cart_buttons
from handlers.keyboards.common import main_menu_keyboard
from handlers.keyboards.orders import (
    create_order_keyboard,
    generate_payment_link_buttons
)
from handlers.keyboards.products import (
    generate_categories_buttons,
    generate_products_buttons,
    generate_product_buttons
)
