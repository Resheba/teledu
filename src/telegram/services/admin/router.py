# mypy: disable-error-code="union-attr, arg-type"
from typing import TYPE_CHECKING

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from src.database import DatabaseService

from .keyboards import (
    AnswerApproveCallback,
    AnswerDetailCallback,
    AnswerPageCallback,
    create_answer_detail_menu,
    create_answers_menu,
)
from .utils import create_answers_detail_text

if TYPE_CHECKING:
    from src.database.models import Answer

router: Router = Router(name="admin")


# @router.message(F.video)
# async def echo(message: Message) -> None:
#     await message.answer(repr(message.video) or "None?")


@router.message(Command("answers"))
async def get_all_answers(message: Message, manager: DatabaseService) -> None:
    answers: list[Answer] = await manager.get_unapproved_answers()
    await message.answer("Ответы", reply_markup=create_answers_menu(answers))


@router.callback_query(AnswerPageCallback.filter())
async def answers_page(
    query: CallbackQuery,
    callback_data: AnswerPageCallback,
    manager: DatabaseService,
) -> None:
    answers: list[Answer] = await manager.get_unapproved_answers()
    await query.message.edit_reply_markup(
        reply_markup=create_answers_menu(answers, current_page=callback_data.page),
    )


@router.callback_query(AnswerDetailCallback.filter())
async def answer_details(
    query: CallbackQuery,
    callback_data: AnswerDetailCallback,
    manager: DatabaseService,
) -> None:
    answer: Answer | None = await manager.get_answer(callback_data.answer_id)
    if answer is None:
        await query.answer("Ошибка при получении ответа!")
        return
    await query.message.answer_video(
        video=answer.video_answer_id,
        caption=create_answers_detail_text(answer),
        reply_markup=create_answer_detail_menu(answer),
    )


@router.callback_query(AnswerApproveCallback.filter())
async def answer_approve(
    query: CallbackQuery,
    callback_data: AnswerApproveCallback,
    manager: DatabaseService,
) -> None:
    answer: Answer | None = await manager.get_answer(callback_data.answer_id)
    if answer is None:
        await query.answer("Ошибка при получении ответа!")
        return
    if callback_data.is_approved:
        await manager.approve_answer(callback_data.answer_id)
        await query.bot.send_message(answer.user_id, "Ваш ответ одобрен!")
        await query.answer("Ответ одобрен!")
    else:
        await manager.reject_answer(callback_data.answer_id)
        await query.bot.send_message(answer.user_id, "Ваш ответ отклонен!")
        await query.answer("Ответ отклонен!")
    await query.message.delete_reply_markup()
