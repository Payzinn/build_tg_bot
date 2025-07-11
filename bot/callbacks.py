from aiogram.filters.callback_data import CallbackData

class SquareCallback(CallbackData, prefix="area"):
    size: str

class PlotCallback(CallbackData, prefix="plot"):
    availability: str

class BudgetCallback(CallbackData, prefix="budget"):
    budget: str

class TempCallback(CallbackData, prefix="temp"):
    temp: str

class BackCallback(CallbackData, prefix="back"):
    state: str