from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.future import select
from db import User, Lesson
import asyncio


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
                    title=data['lesson_title'],
                    description=data['lesson_description'],
                    content=data['lesson_content'],
                    task=data['lesson_task']
                )

                if await session.merge(lesson):
                    return True
                else:
                    return False, 'Необработанная ошибка'

    except Exception as e:
        return False, e
