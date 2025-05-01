from aiogram.filters.callback_data import CallbackData


class Task5CallbackData(CallbackData, prefix="task5"):
    form: int
