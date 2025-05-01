from aiogram.filters.callback_data import CallbackData


class Task8CallbackData(CallbackData, prefix="task8"):
    form: int
