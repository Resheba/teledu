from aiogram.filters.callback_data import CallbackData


class EducationChapterCallbackData(CallbackData, prefix="edu"):
    id: int
