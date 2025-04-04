from functools import cache

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.config import Texts


def _status_to_icon(status: bool | None) -> str:
    if status is None:
        return ""
    return "✅" if status else "❌"


# def create_menu_keyboard(user_tasks: Iterable[tuple[Task, bool | None]]) -> InlineKeyboardMarkup:
#     return InlineKeyboardMarkup(
#         inline_keyboard=[
#             [
#                 InlineKeyboardButton(
#                     text=f"{_status_to_icon(status)} {task.name}".strip(),
#                     callback_data="ABOBA",
#                 ),
#             ]
#             for task, status in user_tasks
#             if task.name
#         ],
#     )


class EducationMenuCallbackData(CallbackData, prefix="edu"): ...


class MenuCallbackData(CallbackData, prefix="menu"): ...


class EducationChapterCallbackData(CallbackData, prefix="edu"):
    id: int


class MenuKeyboard:
    main_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=callback)]
            for text, callback in (
                ("📖 Обучение", EducationMenuCallbackData().pack()),
                ("📚 Библиотека документов", "library"),
                ("✏️ Сдать экзамен", "exam"),
                ("📞 Контакты", "contact"),
            )
        ],
    )

    @cache
    @staticmethod
    def edu_keyboard(texts: Texts) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=edu.main_button_text,
                        callback_data=EducationChapterCallbackData(id=edu.id).pack(),
                    ),
                ]
                for edu in texts.education.all
            ]
            + [[InlineKeyboardButton(text="◀️ Назад", callback_data=MenuCallbackData().pack())]],
        )
