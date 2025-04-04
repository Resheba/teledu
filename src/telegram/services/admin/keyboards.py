from collections.abc import Sequence

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.database.models import Answer


class AnswerDetailCallback(CallbackData, prefix="detail_answer"):
    answer_id: int


class AnswerPageCallback(CallbackData, prefix="answer_page"):
    page: int


class AnswerApproveCallback(CallbackData, prefix="approve_answer"):
    answer_id: int
    is_approved: bool


def create_answers_menu(
    answers: Sequence[Answer],
    *,
    current_page: int = 0,
) -> InlineKeyboardMarkup:
    page_size: int = 5
    results = [
        [
            InlineKeyboardButton(
                text="answer.user.name",
                callback_data=AnswerDetailCallback(answer_id=answer.id).pack(),
            ),
        ]
        for answer in answers[current_page * page_size : (current_page + 1) * page_size]
        if answer is not None
    ]
    helpers = []
    if current_page != 0:
        helpers.append(
            InlineKeyboardButton(
                text="⬅️",
                callback_data=AnswerPageCallback(page=current_page - 1).pack(),
            ),
        )
    if len(answers) > page_size * (current_page + 1):
        helpers.append(
            InlineKeyboardButton(
                text="➡️",
                callback_data=AnswerPageCallback(page=current_page + 1).pack(),
            ),
        )
    return InlineKeyboardMarkup(
        inline_keyboard=[*results, helpers],
    )


def create_answer_detail_menu(answer: Answer) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Подтвердить",
                    callback_data=AnswerApproveCallback(
                        answer_id=answer.id or 0,
                        is_approved=True,
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text="Отклонить",
                    callback_data=AnswerApproveCallback(
                        answer_id=answer.id or 0,
                        is_approved=False,
                    ).pack(),
                ),
            ],
        ],
    )
