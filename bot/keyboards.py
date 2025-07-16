from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from .callbacks import *
from .dicts import *

start_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔘 Начать", callback_data="begin")]
])

house_types = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔘 Кирпичный", callback_data="brick")],
    [InlineKeyboardButton(text="🔘 Каркасный", callback_data="frame")],
    [InlineKeyboardButton(text="🔘 Модульный", callback_data="module")],
    [InlineKeyboardButton(text="🔘 Ещё не определился", callback_data="undecided")],
    [InlineKeyboardButton(text="🔘 📸 Примеры работ", callback_data="examples")]
])

house_choose = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔘 Да, подходит", callback_data="yes_house")],
    [InlineKeyboardButton(text="🔘 Назад", callback_data="begin")]
])

house_square = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=text, callback_data=SquareCallback(size=value).pack())]
    for text, value in SQUARE_OPTS
]+ [
    [InlineKeyboardButton(text="🔘 Назад", callback_data=BackCallback(state="house_chosen").pack())]
])

house_plot = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=text, callback_data=PlotCallback(availability=value).pack())]
    for text, value in PLOT_OPTS
]+ [
    [InlineKeyboardButton(text="🔘 Назад", callback_data=BackCallback(state="house_square").pack())]
])

house_budget = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=text, callback_data=BudgetCallback(budget=value).pack())]
    for text, value in BUDGET_OPTS
]+ [
    [InlineKeyboardButton(text="🔘 Назад", callback_data=BackCallback(state="plot").pack())]
])

house_temp = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=text, callback_data=TempCallback(temp=value).pack())]
    for text, value in TEMP_OPTS
]+ [
    [InlineKeyboardButton(text="🔘 Назад", callback_data=BackCallback(state="budget").pack())]
])

phone_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔘 Назад", callback_data=BackCallback(state="comment").pack())]
    ]
)

comment_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔘 Пропустить", callback_data="skip")],
            [InlineKeyboardButton(text="🔘 Назад", callback_data=BackCallback(state="temp").pack())]
        ]
    )

admin_start_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔘 Новые Заявки", callback_data=ApplicationCallback(status="new", application_id=0, page=1).pack())],
        [InlineKeyboardButton(text="🔘 Принятые Заявки", callback_data=ApplicationCallback(status="accepted", application_id=0, page=1).pack())]
    ]
)

def get_applications_kb(applications, status: str, page: int, total: int):
    builder = InlineKeyboardBuilder()
    for i, app in enumerate(applications, 1 + (page - 1) * 10):
        builder.add(InlineKeyboardButton(
            text=f"Заявка №{app.id}",
            callback_data=ViewApplicationCallback(status=status, application_id=app.id, page=page).pack()
        ))
    
    total_pages = (total + 9) // 10
    if total_pages > 1:
        if page > 1:
            builder.add(InlineKeyboardButton(
                text="⬅ Назад",
                callback_data=ViewApplicationCallback(status=status, application_id=0, page=page - 1).pack()
            ))
        if page < total_pages:
            builder.add(InlineKeyboardButton(
                text="Следующая ➡",
                callback_data=ViewApplicationCallback(status=status, application_id=0, page=page + 1).pack()
            ))
    builder.adjust(1)
    
    return builder.as_markup()