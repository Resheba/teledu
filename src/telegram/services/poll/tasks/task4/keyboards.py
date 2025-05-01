from aiogram.filters.callback_data import CallbackData


class Task4CallbackData(CallbackData, prefix="task4"):
    form: int
