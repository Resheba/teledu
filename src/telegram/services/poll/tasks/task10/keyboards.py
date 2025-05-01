from aiogram.filters.callback_data import CallbackData


class Task10CallbackData(CallbackData, prefix="task10"):
    form: int
