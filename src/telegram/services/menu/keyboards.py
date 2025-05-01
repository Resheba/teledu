from functools import cache
from typing import Literal

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.config import Settings, Texts
from src.config.resources import DocumentSet
from src.database.models import ChapterAnswerDTO
from src.telegram.services.poll.keyboards import EducationChapterCallbackData


def _status_to_icon(status: bool | Literal["ON_ACC"] | None) -> str:
    if status is None:
        return ""
    if status == "ON_ACC":
        return "⌛️"
    return "✅" if status else "❌"


class EducationMenuCallbackData(CallbackData, prefix="edu"): ...


class MenuCallbackData(CallbackData, prefix="menu"): ...


class LibraryCallbackData(CallbackData, prefix="library"): ...


class DocsCallbackData(CallbackData, prefix="doc"):
    page: int


class MenuKeyboard:
    main_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=callback)]
            for text, callback in (
                ("📖 Обучение", EducationMenuCallbackData().pack()),
                ("📚 Библиотека документов", LibraryCallbackData().pack()),
                ("✏️ Сдать экзамен", "exam"),
            )
        ]
        + [[InlineKeyboardButton(text="📞 Контакты", url=Settings.instance().CONTACT_URL)]],
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

    @staticmethod
    @cache
    def library_keyboard(texts: Texts) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=docset.name,
                        callback_data=DocsCallbackData(page=index).pack(),
                    ),
                ]
                for index, docset in enumerate(texts.documents.all)
            ]
            + [[InlineKeyboardButton(text="◀️ Назад", callback_data=MenuCallbackData().pack())]],
        )

    @staticmethod
    @cache
    def docs_keyboard(docset: DocumentSet) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=doc.name,
                        url=str(doc.url),
                    ),
                ]
                for doc in docset.docs
            ]
            + [
                [
                    InlineKeyboardButton(
                        text="◀️ Назад",
                        callback_data=LibraryCallbackData().pack(),
                    ),
                ],
            ],
        )
