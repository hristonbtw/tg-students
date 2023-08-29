from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram import Bot
from aiogram.types import URLInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv, find_dotenv

from functions import functions as func
from keyboards import keyboards as kb
from state.storage import States

from time import time, strftime, localtime
import os

load_dotenv(find_dotenv())
router = Router()


@router.callback_query()
async def callback_handler(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    user_id = call.from_user.id
    username = call.from_user.username
    chat_id = call.message.chat.id
    admin_id = int(os.getenv('admin'))

    if call.data == "profile":
        #data = func.get_userdata(user_id)

        await call.answer()
        # await call.message.edit_text(text=f"🪪 Ваш профиль:"
        #                                   f"\n\n👤 ФИО: {data[0]}"
        #                                   f"\n🏠 Адрес: {data[1]}"
        #                                   f"\n☎️Номер телефона: {data[2]}"
        #                                   f"\n📦 Курьерская служба: {data[3]}",
        #                              reply_markup=kb.profile_menu)
