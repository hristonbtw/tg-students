from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.future import select
from sqlalchemy import update

from db import User, Lesson
from keyboards import keyboards as kb

from typing import Union
from aiogram import Bot


async def check_access(user_id, session_maker: async_sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            row = await session.execute(select(User.role).where(User.user_id == user_id))
            if row.scalars().first() == 'moderator':
                return True


async def get_userdata(user_id: int, session_maker: async_sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            row = await session.execute(text("select * from users where user_id = {}".format(user_id)))
            for user_obj in row:
                data = {'user_id': user_obj.user_id,
                        'username': user_obj.username,
                        'first_name': user_obj.first_name,
                        'second_name': user_obj.second_name,
                        'role': user_obj.role}

                return data


async def create_lesson(data, session_maker: async_sessionmaker):
    try:
        async with session_maker() as session:
            async with session.begin():
                lesson: Lesson = Lesson(
                    title=data['title'],
                    description=data['description'],
                    content=data['content'],
                    task=data['task'],
                    task_filename=data['filename']
                )

                if await session.merge(lesson):
                    return True
                else:
                    return False, 'Необработанная ошибка'

    except Exception as e:
        return False, e


async def get_all_lessons(session_maker):
    async with session_maker() as session:
        async with session.begin():
            row = await session.execute(text("select id, title from lessons"))
            data = {}
            for lesson_id, title in row:
                data[lesson_id] = title

            keyboard = kb.select_lesson_menu(data=data)

            return keyboard


async def get_lesson_data(lesson_id, session_maker):
    async with session_maker() as session:
        async with session.begin():
            row = await session.execute(text("select * from lessons where id = {}".format(lesson_id)))

            for lesson_obj in row:
                data = {'id': lesson_obj.id,
                        'title': lesson_obj.title,
                        'description': lesson_obj.description,
                        'content': lesson_obj.content,
                        'task': lesson_obj.task,
                        'task_filename': lesson_obj.task_filename}

            return data


async def edit_lesson_data(option: str, lesson_id: int, data: Union[str, bytes],
                           filename: Union[str, None], session_maker: async_sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            if option == "title":
                if await session.execute(update(Lesson).values(title=data).where(Lesson.id == lesson_id)):
                    return True
                else:
                    return False, 'Не удалось обновить название урока'
            elif option == "description":
                if await session.execute(update(Lesson).values(description=data).where(Lesson.id == lesson_id)):
                    return True
                else:
                    return False, 'Не удалось обновить описание урока'
            elif option == "content":
                if await session.execute(update(Lesson).values(content=data).where(Lesson.id == lesson_id)):
                    return True
                else:
                    return False, 'Не удалось обновить контент урока'
            elif option == "task":
                if await session.execute(
                        update(Lesson).values(task=data, task_filename=filename).where(Lesson.id == lesson_id)
                ):

                    return True
                else:
                    return False, 'Не удалось обновить задание урока'


async def get_file_data(message, bot: Bot):
    file = await bot.get_file(message.document.file_id)
    result = await bot.download_file(file.file_path)
    filename = message.document.file_name
    output_bytes = result.read()

    row = {'task': output_bytes,
           'task_filename': filename}

    return row
