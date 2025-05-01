from aiogram.filters.callback_data import CallbackData


class Task9CallbackData(CallbackData, prefix="task9"):
    form: int
