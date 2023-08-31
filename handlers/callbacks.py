from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram import Bot
from aiogram.types import URLInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv, find_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker

from functions import functions as func
from keyboards import keyboards as kb
from state.storage import States

from time import time, strftime, localtime
import os

load_dotenv(find_dotenv())
router = Router()


@router.callback_query()
async def callback_handler(call: types.CallbackQuery, state: FSMContext, bot: Bot, session_maker: async_sessionmaker):
    user_id = call.from_user.id
    username = call.from_user.username
    chat_id = call.message.chat.id

    if call.data == "profile":
        data = await func.get_userdata(user_id, session_maker=session_maker)

        await call.answer()


    if call.data == "mod_menu":
        await call.answer()

        if await func.check_access(user_id=user_id, session_maker=session_maker):
            await call.message.edit_text("Вы перешли в меню модератора",
                                         reply_markup=kb.mod_menu)
        else:
            await call.message.edit_text("Вы не модератор.",
                                         reply_markup=kb.main_menu)

