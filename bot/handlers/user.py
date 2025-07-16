from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from ..texts import *
from ..keyboards import *
from ..states import House
from ..dicts import *
from datetime import datetime, timedelta
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardBuilder
from aiogram.fsm.storage.base import StorageKey
from ..db.models import *
from ..db.database import *

router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()
    username = message.from_user.username
    fullname = message.from_user.full_name
    user_tg_id = message.from_user.id
    if not await user_exists(user_tg_id):
        if username:
            await add_user(user_tg_id, username)
        else:
            await add_user(user_tg_id, fullname)
    await message.answer(text=start_message, parse_mode="HTML", reply_markup=start_keyboard, disable_web_page_preview=True)


@router.callback_query(F.data == "begin")
async def begin(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(text=hello_message, reply_markup=house_types)

@router.callback_query(F.data == "examples")
async def examples(callback: CallbackQuery, state: FSMContext):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔘 Да", callback_data="begin")],
        [InlineKeyboardButton(text="🔘 Выйти", callback_data="begin")]
    ])
    await callback.message.edit_text(text=examples_message, parse_mode="HTML", reply_markup=keyboard, disable_web_page_preview=True)

@router.callback_query(lambda c: c.data in HOUSE_TYPES)
async def house(callback: CallbackQuery, state: FSMContext):
    await state.set_state(House.house_chosen)
    chosen_house_type, message_text = HOUSE_TYPES[callback.data]
    if callback.data == "undecided":
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔘 Да", callback_data="yes_house")],
            [InlineKeyboardButton(text="🔘 Выйти", callback_data="begin")],
        ])
        await callback.message.edit_text(text=message_text, reply_markup=keyboard)
    else:
        await callback.message.edit_text(text=message_text, reply_markup=house_choose)
    await state.update_data(house_chosen=chosen_house_type)

@router.callback_query(F.data == "yes_house")
async def square(callback:CallbackQuery, state:FSMContext):
    await state.set_state(House.house_square)
    await callback.message.edit_text(text="Примерная площадь дома?", reply_markup=house_square)

@router.callback_query(SquareCallback.filter())
async def plot(callback: CallbackQuery, callback_data: SquareCallback,state: FSMContext):
    await state.update_data(house_square=callback_data.size)
    await callback.message.edit_text(text="У вас уже есть участок под строительство?", reply_markup=house_plot)
    await state.set_state(House.plot)

@router.callback_query(PlotCallback.filter())
async def budget(callback:CallbackQuery, callback_data: PlotCallback, state: FSMContext):
    await state.update_data(plot=callback_data.availability)
    await callback.message.edit_text(text="Какой ориентировочный бюджет?", reply_markup=house_budget)
    await state.set_state(House.budget)

@router.callback_query(BudgetCallback.filter())
async def temp(callback: CallbackQuery, callback_data: BudgetCallback, state: FSMContext):
    await state.update_data(budget=callback_data.budget)
    await callback.message.edit_text(text="Сроки:", reply_markup=house_temp)
    await state.set_state(House.temp)

@router.callback_query(TempCallback.filter())
async def comments(callback: CallbackQuery, callback_data: TempCallback, state: FSMContext):
    await state.update_data(temp=callback_data.temp)
    await callback.message.edit_text("Хотите оставить комментарий, пожелания или задать вопрос?\n(Можно пропустить)", reply_markup=comment_keyboard)
    await state.set_state(House.comment)

@router.message(House.comment, F.text)
async def phone(message: Message, state: FSMContext):
    await state.update_data(comment=message.text)
    await state.set_state(House.phone)
    await message.answer(text=contacts_message, reply_markup=phone_keyboard)

@router.callback_query(House.comment, F.data == "skip")
async def skip_comm(callback: CallbackQuery, state: FSMContext):
    await state.update_data(comment=None)
    await state.set_state(House.phone)
    await callback.message.edit_text(text=contacts_message, reply_markup=phone_keyboard)

@router.message(House.phone)
async def name(message: Message, state: FSMContext):
    if message.text and message.text.startswith("8") and len(message.text) == 11 and message.text.isalnum:
        await state.update_data(phone=message.text)
    else:
        await message.answer("❌ Номер телефона должен начинаться с 8 и не превышать 11 символов!\nВведите номер телефона заново:", reply_markup=phone_keyboard)
        return
    
    await state.set_state(House.name)
    await message.answer("🧑 Как вас зовут?")

@router.message(House.name)
async def final(message: Message, state: FSMContext):
    if message.text and message.text.isalpha():
        await state.update_data(name=message.text)
        data = await state.get_data()

        name = data.get("name")
        house_chosen = data.get("house_chosen")
        house_square = data.get("house_square")
        plot = data.get("plot")
        budget = data.get("budget")
        temp = data.get("temp")
        comment = data.get("comment", "Пропущено")
        phone = data.get("phone")

        username = message.from_user.username
        fullname = message.from_user.full_name
        user_tg_id = message.from_user.id
        user = await user_exists(user_tg_id)
        user_get = await get_user(user_tg_id)
        if not user and not user_get:
            if username:
                await add_user(user_tg_id, username)
            else:
                await add_user(user_tg_id, fullname)

        house_chosen = next((text for text, (_, _) in HOUSE_TYPES.items() if text == house_chosen), house_chosen)
        house_square = next((text for text, value in SQUARE_OPTS if value == house_square), house_square)
        plot = next((text for text, value in PLOT_OPTS if value == plot), plot)
        budget = next((text for text, value in BUDGET_OPTS if value == budget), budget)
        temp = next((text for text, value in TEMP_OPTS if value == temp), temp)

        await add_application(user_id=user_get.id, username_app=name, house_chosen = house_chosen, house_square = house_square, plot = plot, budget = budget, temp=temp, comment=comment, phone = phone)
        await message.answer(f"Спасибо, {name}! Мы получили вашу заявку.\nНаш специалист свяжется с вами в ближайшее время\n\n📸 Пока можно посмотреть ещё примеры работ:\n👉 <a href='website-kzn.ru'>Посмотреть</a>", parse_mode="HTML", disable_web_page_preview=True)
        await state.clear()
    else:
        await message.answer("Имя должно состоять из букв!\nВведите имя ещё раз: ")
        return

@router.callback_query(BackCallback.filter())
async def go_back(callback: CallbackQuery, callback_data: BackCallback, state: FSMContext):
    current_state = await state.get_state()
    if not current_state:
        await callback.answer("Нет предыдущего шага!")
        return

    state_map = {
        "House:house_square": ("House:house_chosen", house_types, hello_message),
        "House:plot": ("House:house_square", house_square, "Примерная площадь дома?"),
        "House:budget": ("House:plot", house_plot, "У вас уже есть участок под строительство?"),
        "House:temp": ("House:budget", house_budget, "Какой ориентировочный бюджет?"),
        "House:comment": ("House:temp", house_temp, "Сроки:"),
        "House:phone": ("House:comment", comment_keyboard, "Хотите оставить комментарий, пожелания или задать вопрос?\n(Можно пропустить)"),
    }
    prev_state, prev_keyboard, prev_message = state_map.get(current_state, (None, None, None))

    if prev_state:
        await state.set_state(prev_state)
        await callback.message.edit_text(text=prev_message, reply_markup=prev_keyboard)