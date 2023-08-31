from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from functions import functions as func

main_menu = InlineKeyboardBuilder()
main_menu.button(text="👨🏻‍💻 Профиль", callback_data="profile")
main_menu.button(text="🔧 Меню модератора", callback_data="mod_menu")
main_menu.adjust(2, 2)
main_menu = main_menu.as_markup()

mod_menu = InlineKeyboardBuilder()
mod_menu.button(text="Добавить товар", callback_data="add_product")
mod_menu.button(text="Сделать рассылку", callback_data="make_messages")
mod_menu.button(text="Изменить статус заказа", callback_data="change_status")
mod_menu = mod_menu.as_markup()

go_back_menu = InlineKeyboardBuilder()
go_back_menu.button(text="🔙 Назад", callback_data="go_back")
go_back_menu = go_back_menu.as_markup()
