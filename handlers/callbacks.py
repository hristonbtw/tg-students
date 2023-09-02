from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram import Bot
from aiogram.types import URLInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv, find_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker

from functions import functions as func
from keyboards import keyboards as kb
from state.storage import Lesson

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
