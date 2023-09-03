from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram import Bot
from aiogram.types.input_file import BufferedInputFile
from aiogram.exceptions import TelegramBadRequest
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv, find_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker

from functions import functions as func
from keyboards import keyboards as kb
from state.storage import Lesson, EditLesson

from time import time, strftime, localtime
import os

load_dotenv(find_dotenv())
router = Router()


@router.callback_query()
async def callback_handler(call: types.CallbackQuery, state: FSMContext, bot: Bot, session_maker: async_sessionmaker):
    user_id = int(call.from_user.id)
    username = call.from_user.username

    if call.data == "profile":
        await call.answer()
        data = await func.get_userdata(user_id, session_maker=session_maker)

        user_id = data['user_id']
        username = data['username']
        first_name = data['first_name']
        second_name = data['second_name']
        role = data['role']

        await call.message.edit_text(f'Ваш профиль:'
                                     f'\n\nID: {user_id}'
                                     f'\nЮзернейм: {username}'
                                     f'\nИмя: {first_name}'
                                     f'\nФамилия: {second_name}'
                                     f'\nРоль: {role}',
                                     reply_markup=kb.go_back_menu)

    if call.data == "mod_menu":
        await call.answer()

        if await func.check_access(user_id=user_id, session_maker=session_maker):
            await call.message.edit_text("Вы перешли в меню модератора",
                                         reply_markup=kb.mod_menu)
        else:
            await call.message.edit_text("Вы не модератор.",
                                         reply_markup=kb.main_menu)

    if call.data == "go_back":
        await call.answer()

        await call.message.edit_text("Вы вернулись в главное меню",
                                     reply_markup=kb.main_menu)

    if call.data == "add_lesson":
        await call.answer()

        await state.set_state(Lesson.title)
        await call.message.answer("Введите название урока")

    if call.data == "edit_lesson":
        await call.answer()

        lessons_keyboard = await func.get_all_lessons(session_maker=session_maker)
        await call.message.edit_text(text='Выберите урок:', reply_markup=lessons_keyboard)

    if call.data.startswith('edit_lesson_'):
        await call.answer()

        lesson_id = int(call.data.split("_")[2])
        lesson_data = await func.get_lesson_data(lesson_id=lesson_id, session_maker=session_maker)
        lesson_file = BufferedInputFile(file=lesson_data['task'], filename=lesson_data['task_filename'])

        try:
            await call.message.answer_video(lesson_data["content"], caption="Контент:")

            await call.message.answer_document(document=lesson_file,
                                               caption=f'Название урока: "{lesson_data["title"]}"'
                                                       f'\nОписание урока: {lesson_data["description"]}'
                                                       f'\nЗадание: ',
                                               reply_markup=kb.edit_lesson_menu(lesson_id=lesson_id))

        except TelegramBadRequest:
            await call.message.answer_document(document=lesson_file,
                                               caption=f'Название урока: "{lesson_data["title"]}"'
                                                       f'\nОписание урока: {lesson_data["description"]}'
                                                       f'\nКонтент: {lesson_data["content"]}'
                                                       f'\nЗадание: ',
                                               reply_markup=kb.edit_lesson_menu(lesson_id=lesson_id))

    if call.data.startswith('change_lesson_'):
        await call.answer()

        lesson_id = int(call.data.split("_")[3])
        option = call.data.split("_")[2]

        await state.update_data(option=option)
        await state.update_data(lesson_id=lesson_id)

        if option == 'title':
            await state.set_state(EditLesson.title)

            await call.message.answer("Введите новое название урока")
        elif option == 'description':
            await state.set_state(EditLesson.description)

            await call.message.answer("Введите новое описание урока")
        elif option == 'content':
            await state.set_state(EditLesson.content)

            await call.message.answer("Отправьте новый контент для урока")
        elif option == 'task':
            await state.set_state(EditLesson.task)

            await call.message.answer("Отправьте новое задание для урока")
