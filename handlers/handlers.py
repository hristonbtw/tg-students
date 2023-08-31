from aiogram.filters.command import Command
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram import Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards import keyboards as kb
from functions import functions as func
from middlewares.register_check import RegisterCheck
from state.storage import States
from sqlalchemy.ext.asyncio import async_sessionmaker

import os
from dotenv import load_dotenv

load_dotenv()
router = Router()
router.message.middleware(RegisterCheck())


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("qq 👋\n\nВыбери опции ниже:",
                         reply_markup=kb.main_menu)


@router.message(Command("admin"))
async def cmd_admin(message: types.Message):
    user_id = message.from_user.id
    if user_id == int(os.getenv('admin')):
        await message.answer('Вы перешли в меню админа',
                             reply_markup=kb.admin_menu)

