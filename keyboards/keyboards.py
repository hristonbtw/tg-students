from aiogram.utils.keyboard import InlineKeyboardBuilder

main_menu = InlineKeyboardBuilder()
main_menu.button(text="👨🏻‍💻 Профиль", callback_data="profile")
main_menu.adjust(2, 2)
main_menu = main_menu.as_markup()

mod_menu = InlineKeyboardBuilder()
mod_menu.button(text="Добавить урок", callback_data="add_lesson")
mod_menu.button(text="Редактировать урок", callback_data="edit_lesson")
mod_menu.button(text="Удалить урок", callback_data="remove_lesson")
mod_menu.adjust(2, 2)
mod_menu = mod_menu.as_markup()

go_back_menu = InlineKeyboardBuilder()
go_back_menu.button(text="🔙 Назад", callback_data="go_back")
go_back_menu = go_back_menu.as_markup()


async def select_lesson_menu(option, data):
    lesson_menu = InlineKeyboardBuilder()

    if option == "edit":

        for i in data:
            lesson_menu.button(text=data[i], callback_data=f'edit_lesson_{i}')

    elif option == "remove":

        for i in data:
            lesson_menu.button(text=data[i], callback_data=f'remove_lesson_{i}')

    lesson_menu.button(text="Назад", callback_data="go_back_mod")
    lesson_menu.adjust(2, 2)
    return lesson_menu.as_markup()


async def edit_lesson_menu(lesson_id):
    edit_lesson = InlineKeyboardBuilder()
    edit_lesson.button(text='Изменить название урока', callback_data=f'change_lesson_title_{lesson_id}')
    edit_lesson.button(text='Изменить описание урока', callback_data=f'change_lesson_description_{lesson_id}')
    edit_lesson.button(text='Изменить контент урока', callback_data=f'change_lesson_content_{lesson_id}')
    edit_lesson.button(text='Изменить задание урока', callback_data=f'change_lesson_task_{lesson_id}')
    edit_lesson.button(text='Назад', callback_data=f'go_back_mod')
    edit_lesson.adjust(2, 2)

    return edit_lesson.as_markup()
