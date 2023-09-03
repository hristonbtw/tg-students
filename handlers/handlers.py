import io

from aiogram.filters.command import Command
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram import Bot
from aiogram.types.input_file import BufferedInputFile
from aiogram.types import InputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards import keyboards as kb
from functions import functions as func
from middlewares.register_check import RegisterCheck
from state.storage import Lesson, EditLesson
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
async def set_lesson_name(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(Lesson.description)

    await message.answer("Введите описание урока")


@router.message(Lesson.description)
async def set_lesson_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(Lesson.content)

    print(message)

    await message.answer("Добавьте видеофайл или zoom-ссылку")


@router.message(Lesson.content)
async def set_lesson_content(message: types.Message, state: FSMContext):
    await state.update_data(content=message.text)
    await state.set_state(Lesson.task)

    await message.answer("Добавьте файл (док или таблица")


@router.message(Lesson.task)
async def set_lesson_content(message: types.Message, state: FSMContext, bot: Bot, session_maker: async_sessionmaker):
    # Тестирую бинарное "скачивание" файлов, дабы не занимать пространство и директории на локальной машине
    # Планирую подгружать из бд байты и отправлять их студентам

    file_data = await func.get_file_data(message=message, bot=bot)

    await state.update_data(task=file_data['task'], filename=file_data['task'])
    data = await state.get_data()

    is_lesson_created = await func.create_lesson(data, session_maker=session_maker)

    if is_lesson_created is True:
        input_file = BufferedInputFile(file_data['task'], filename=file_data['filename'])
        await message.answer_document(input_file,
                                      caption=f'Урок успешно создан:'
                                              f'\n\nНазвание: "{data["title"]}"'
                                              f'\nОписание: {data["description"]}'
                                              f'\nКонтент: {data["content"]}'
                                              f'\n\nЗадание: ',
                                      reply_marku=kb.mod_menu)
    else:
        await message.answer(f"Что-то пошло не так. Ошибка: {is_lesson_created[1]}")


@router.message(EditLesson.title)
async def edit_lesson_title(message: types.Message, state: FSMContext, session_maker: async_sessionmaker):
    await state.update_data(title=message.text)
    data = await state.get_data()

    is_lesson_changed = await func.edit_lesson_data(option=data['option'],
                                                    lesson_id=data['lesson_id'],
                                                    data=data['title'],
                                                    filename=None,
                                                    session_maker=session_maker)

    if is_lesson_changed is True:
        await message.answer(f'Вы успешно изменили название урока на "{data["title"]}"')
    else:
        await message.answer(f"Что-то пошло не так. Ошибка: {is_lesson_changed[1]}")


@router.message(EditLesson.description)
async def edit_lesson_description(message: types.Message, state: FSMContext, session_maker: async_sessionmaker):
    await state.update_data(description=message.text)
    data = await state.get_data()

    is_lesson_changed = await func.edit_lesson_data(option=data['option'],
                                                    lesson_id=data['lesson_id'],
                                                    data=data['description'],
                                                    filename=None,
                                                    session_maker=session_maker)

    if is_lesson_changed is True:
        await message.answer(f'Вы успешно изменили описание урока на "{data["description"]}"')
    else:
        await message.answer(f'Что-то пошло не так. Ошибка: {is_lesson_changed[1]}')


@router.message(EditLesson.content)
async def edit_lesson_content(message: types.Message, state: FSMContext, session_maker: async_sessionmaker):
    if message.video:
        video_id = message.video.file_id

        await state.update_data(video_id=video_id)
        data = await state.get_data()

        is_lesson_changed = await func.edit_lesson_data(option=data['option'],
                                                        lesson_id=data['lesson_id'],
                                                        data=data['video_id'],
                                                        filename=None,
                                                        session_maker=session_maker)

        if is_lesson_changed is True:
            await message.answer_video(video=video_id, caption="Вы успешно изменили контент на видео выше",
                                       reply_markup=kb.mod_menu)
        else:
            await message.answer(f"Что-то пошло не по плану. Ошибка: {is_lesson_changed[1]}")
    else:

        link = message.text

        await state.update_data(link=link)
        data = await state.get_data()

        is_lesson_changed = await func.edit_lesson_data(option=data['option'],
                                                        lesson_id=data['lesson_id'],
                                                        data=data['link'],
                                                        filename=None,
                                                        session_maker=session_maker)

        if is_lesson_changed is True:
            await message.answer(f'Вы успешно изменили контент на: "{link}"',
                                 reply_markup=kb.mod_menu)
        else:
            await message.answer(f'Что-то пошло не по плану. Ошибка {is_lesson_changed[1]}')


@router.message(EditLesson.task)
async def edit_lesson_content(message: types.Message, state: FSMContext, bot: Bot, session_maker: async_sessionmaker):
    file_data = await func.get_file_data(message=message, bot=bot)

    await state.update_data(task=file_data['task'], task_filename=file_data['task_filename'])
    data = await state.get_data()

    is_lesson_changed = await func.edit_lesson_data(option=data['option'],
                                                    lesson_id=data['lesson_id'],
                                                    data=data['task'],
                                                    filename=data['task_filename'],
                                                    session_maker=session_maker)

    if is_lesson_changed is True:
        file = BufferedInputFile(file_data['task'], filename=file_data['task_filename'])

        await message.answer("Вы успешно изменили задание:")
        await message.answer_document(file)

    else:
        await message.answer(f"Что-то пошло не так. Ошибка: {is_lesson_changed[1]}")
