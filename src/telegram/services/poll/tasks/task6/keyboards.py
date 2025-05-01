from aiogram.filters.callback_data import CallbackData


class Task6CallbackData(CallbackData, prefix="task6"):
    form: int
