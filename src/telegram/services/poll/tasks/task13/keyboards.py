from aiogram.filters.callback_data import CallbackData


class Task13CallbackData(CallbackData, prefix="task13"):
    form: int
