from typing import Literal

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.database.models import ChapterAnswerDTO
from src.telegram.services.poll.keyboards import EducationChapterCallbackData


def _status_to_icon(status: bool | Literal["ON_ACC"] | None) -> str:
    if status is None:
        return ""
    if status == "ON_ACC":
        return "⌛️"
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

    @staticmethod
    def edu_keyboard(chapters: list[ChapterAnswerDTO]) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=(_status_to_icon(edu.is_approved) + " " + edu.name).strip(),
                        callback_data=EducationChapterCallbackData(id=edu.id).pack(),
                    ),
                ]
                for edu in chapters
            ]
            + [[InlineKeyboardButton(text="◀️ Назад", callback_data=MenuCallbackData().pack())]],
        )
