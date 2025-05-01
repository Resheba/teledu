from aiogram.filters.callback_data import CallbackData


class Task12CallbackData(CallbackData, prefix="task12"):
    form: int
