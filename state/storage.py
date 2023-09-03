from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.callback_data import CallbackData
from typing import Optional

storage = MemoryStorage()


class Lesson(StatesGroup):
    title = State()
    description = State()
    content = State()
    task = State()
    filename = State()


class EditLesson(StatesGroup):
    title = State()
    description = State()
    content = State()
    task = State()
    filename = State()
    option = State()
    lesson_id = State()
