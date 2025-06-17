from aiogram.filters.callback_data import CallbackData


class Task2CallbackData(CallbackData, prefix="task2"):
    form: int
