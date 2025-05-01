from aiogram.filters.callback_data import CallbackData


class Task7CallbackData(CallbackData, prefix="task7"):
    form: int
