import asyncio
import logging
import os
from dotenv import load_dotenv
from sqlalchemy import URL

from state import storage
from handlers import handlers, callbacks
from db import BaseModel, create_async_engine, get_session_maker, proceed_schemas

from aiogram import Bot, Dispatcher


load_dotenv()
token = os.getenv('token')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=token)
dp = Dispatcher(storage=storage.storage)


async def main():

    postgres_url = URL.create(
        "postgresql+asyncpg",
        username="postgres",
        host="localhost",
        database="postgres",
        password="e1117890",
        port=5432
    )

    async_engine = create_async_engine(postgres_url)
    session_maker = get_session_maker(async_engine)
    await proceed_schemas(async_engine, BaseModel.metadata)

    dp.include_router(handlers.router)
    dp.include_router(callbacks.router)

    await dp.start_polling(bot, session_maker=session_maker)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Отключаюсь..')
