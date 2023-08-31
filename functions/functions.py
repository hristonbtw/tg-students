from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.future import select
from db import User
import asyncio


async def check_access(user_id, session_maker: async_sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            row = await session.execute(select(User.role).where(User.user_id == user_id))
            if row.scalars().first() == 'moderator':
                return True


async def get_userdata(user_id, session_maker: async_sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            row = await session.execute(select(User).where(User.user_id == user_id))
            print(row.scalars().all())
            return row
