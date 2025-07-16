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

class ApplicationCallback(CallbackData, prefix="app"):
    status: str
    application_id: int
    page: int

class ViewApplicationCallback(CallbackData, prefix="view_app"):
    application_id: int
    page: int
    status: str

class UpdateApplicationStatusCallback(CallbackData, prefix="update_app"):
    application_id: int
    status: str
    page: int