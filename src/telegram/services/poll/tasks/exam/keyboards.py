from aiogram.filters.callback_data import CallbackData


class ExamCallbackData(CallbackData, prefix="exam"):
    form: int
