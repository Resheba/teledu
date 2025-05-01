from aiogram.filters.callback_data import CallbackData


class Task11CallbackData(CallbackData, prefix="task11"):
    form: int
