from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from functions import functions as func

main_menu = InlineKeyboardBuilder()
main_menu.button(text="👨🏻‍💻 Профиль", callback_data="profile")
main_menu.button(text="🛒 Одежда", callback_data="clothes")
main_menu.button(text="🆘 Помощь", callback_data="help")
main_menu.button(text="⭐ Отзывы", url="https://t.me/deadline_reviews")
main_menu.button(text="📦 Мои заказы", callback_data="my_orders")
main_menu.adjust(2, 2)
main_menu = main_menu.as_markup()

admin_menu = InlineKeyboardBuilder()
admin_menu.button(text="Добавить товар", callback_data="add_product")
admin_menu.button(text="Сделать рассылку", callback_data="make_messages")
admin_menu.button(text="Изменить статус заказа", callback_data="change_status")
admin_menu = admin_menu.as_markup()
