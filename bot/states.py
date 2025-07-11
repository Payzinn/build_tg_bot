from aiogram.filters.state import (StatesGroup, State)
from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

class House(StatesGroup):
    house_chosen = State()
    house_square = State()
    plot = State()
    budget = State()
    temp = State()
    comment = State()
    phone = State()
    name = State()
    