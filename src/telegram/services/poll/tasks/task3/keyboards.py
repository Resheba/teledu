from aiogram.filters.callback_data import CallbackData


class Task3CallbackData(CallbackData, prefix="task3"):
    form: int
