import io

from aiogram.filters.command import Command
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram import Bot
from aiogram.types.input_file import BufferedInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards import keyboards as kb
from functions import functions as func
from middlewares.register_check import RegisterCheck
from state.storage import Lesson
from sqlalchemy.ext.asyncio import async_sessionmaker

import os
from dotenv import load_dotenv

load_dotenv()
router = Router()
router.message.middleware(RegisterCheck())


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет 👋\n\nВыбери опции ниже:",
                         reply_markup=kb.main_menu)


@router.message(Command("mod"))
async def cmd_admin(message: types.Message, session_maker: async_sessionmaker):
    user_id = message.from_user.id
    data = await func.get_userdata(user_id, session_maker=session_maker)
    if data['role'] == 'moderator':
        await message.answer("Вы перешли в меню модератора",
                             reply_markup=kb.mod_menu)
    else:
        await message.answer("Вы не модератор",
                             reply_markup=kb.main_menu)


@router.message(Lesson.title)
async def set_lesson_name(message: types.Message, bot: Bot, state: FSMContext):
    await state.update_data(lesson_title=message.text)
    await state.set_state(Lesson.description)

    # Тестирую бинарное "скачивание" файлов, дабы не занимать пространство и директории на локальной машине
    # Планирую подгружать из бд байты и отправлять их студентам

    file = await bot.get_file(message.document.file_id)
    result = await bot.download_file(file.file_path)
    filename = message.document.file_name
    print(filename)

    output_bytes = result.read()
    input_file: BufferedInputFile = BufferedInputFile(output_bytes, filename=filename)
    await message.answer_document(input_file, caption='Отправлено.')


@router.message(Lesson.description)
async def set_lesson_description(message: types.Message, state: FSMContext):
    await state.update_data(lesson_description=message.text)
    await state.set_state(Lesson.content)

    await message.answer("Добавьте видеофайл или zoom-ссылку")


@router.message(Lesson.content)
async def set_lesson_content(message: types.Message, state: FSMContext):
    await state.update_data(lesson_content=message.text)
    await state.set_state(Lesson.task)

    await message.answer("Добавьте файл (док или таблица")


@router.message(Lesson.task)
async def set_lesson_content(message: types.Message, state: FSMContext, session_maker: async_sessionmaker):
    await state.update_data(lesson_task=message.text)
    data = await state.get_data()

    is_lesson_created = await func.create_lesson(data, session_maker=session_maker)

    if is_lesson_created:
        await message.answer(f'Вы успешно создали урок:'
                             f'\n\nНазвание: "{data["lesson_title"]}"'
                             f'\nОписание: {data["lesson_description"]}'
                             f'\nВидео-файл или zoom-ссылка: {data["lesson_content"]}'
                             f'\nЗадание: {data["lesson_task"]}',
                             reply_markup=kb.mod_menu)
    else:
        await message.answer(f"Что-то пошло не так. Ошибка: {is_lesson_created[1]}")
