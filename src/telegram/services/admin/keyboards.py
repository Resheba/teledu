from collections.abc import Iterable

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.database.models import UnapprovedAnswerDTO, User


class ApproveCallbackData(CallbackData, prefix="appr"):
    page: int


class ApproveUserCallbackData(CallbackData, prefix="userappr"):
    user_id: int


class AnswerCallbackData(CallbackData, prefix="ans"):
    answer_id: int


class ApproveAnswerCallbackData(CallbackData, prefix="ansappr"):
    user_id: int
    answer_id: int
    is_approved: bool


class AdminKeyboard:
    @staticmethod
    def user_unapproved_keyboard(answers: Iterable[UnapprovedAnswerDTO]) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="📍 " + answer.chapter_name,
                        callback_data=AnswerCallbackData(answer_id=answer.answer_id).pack(),
                    ),
                ]
                for answer in answers
            ]
            + [[InlineKeyboardButton(text="⬅️", callback_data=ApproveCallbackData(page=0).pack())]],
        )

    @staticmethod
    def approves_keyboard(
        users: list[tuple[User, int]],
        *,
        current_page: int = 0,
    ) -> InlineKeyboardMarkup:
        page_size: int = 6
        results = [
            [
                InlineKeyboardButton(
                    text=f"({count}) {user.name}",
                    callback_data=ApproveUserCallbackData(user_id=user.telegram_id).pack(),
                ),
            ]
            for user, count in users[current_page * page_size : (current_page + 1) * page_size]
        ]
        helpers = []
        if current_page != 0:
            helpers.append(
                InlineKeyboardButton(
                    text="⬅️",
                    callback_data=ApproveCallbackData(page=current_page - 1).pack(),
                ),
            )
        if len(users) > page_size * (current_page + 1):
            helpers.append(
                InlineKeyboardButton(
                    text="➡️",
                    callback_data=ApproveCallbackData(page=current_page + 1).pack(),
                ),
            )
        return InlineKeyboardMarkup(
            inline_keyboard=[*results, helpers],
        )

    @staticmethod
    def answer_keyboard(answer_id: int, user_id: int) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="✅",
                        callback_data=ApproveAnswerCallbackData(
                            answer_id=answer_id,
                            is_approved=True,
                            user_id=user_id,
                        ).pack(),
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="❌",
                        callback_data=ApproveAnswerCallbackData(
                            answer_id=answer_id,
                            is_approved=False,
                            user_id=user_id,
                        ).pack(),
                    ),
                ],
            ],
        )
