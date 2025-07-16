from .texts import *

SQUARE_OPTS = [
    ("🔘 до 100 м²", "lt100"),
    ("🔘 100–150 м²", "100_150"),
    ("🔘 150–200 м²", "150_200"),
    ("🔘 более 200 м²", "gt200"),
    ("🔘 Пока не знаю", "unknown"),
]


HOUSE_TYPES = {
    "brick": ("Кирпичный", brick_message),
    "module": ("Модульный", module_message),
    "frame": ("Каркасный", frame_message),
    "undecided": ("Ещё не определился", undecided_message),
}

PLOT_OPTS = [
    ("🔘 Да", "yes_plot"),
    ("🔘 В процессе покупки", "plot_buy_process"),
    ("🔘 Пока нет", "no_plot"),
    ("🔘 Нужна помощь с подбором", "need_help")
]

BUDGET_OPTS = [
    ("🔘 до 3 млн ₽", "3mil"),
    ("🔘 3-5 млн ₽", "3_5"),
    ("🔘 5-8 млн ₽", "5_8"),
    ("🔘 более 8 млн ₽", "gt8"),
    ("🔘 Пока не решил(а)", "unknown"),
]

TEMP_OPTS = [
    ("🔘 В ближайшие 1–2 месяца ", "1_2"),
    ("🔘 Через 3-6 месяцев", "3_6"),
    ("🔘 Через год", "year"),
    ("🔘 Просто интересуюсь", "interested")
]

STATUS_OPTS = [
    ("🔘 Новые заявки", "new"),
    ("🔘 Принятые заявки", "accepted"),
]

STATUS_MAP = {value: name for name, value in STATUS_OPTS}