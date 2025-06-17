from aiogram.filters.callback_data import CallbackData


class Task1CallbackData(CallbackData, prefix="task1"):
    form: int
