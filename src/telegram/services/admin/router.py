from typing import TYPE_CHECKING

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import CallbackQuery, InputMediaVideo, Message

from src.database import DatabaseService

from .filters import IsAdmin
from .keyboards import (
    AdminKeyboard,
    AnswerCallbackData,
    ApproveAnswerCallbackData,
    ApproveCallbackData,
    ApproveUserCallbackData,
)

if TYPE_CHECKING:
    from src.database.models import User


router: Router = Router(name="admin")
router.message.filter(IsAdmin())
router.callback_query.filter(IsAdmin())


@router.message(Command("approves"), StateFilter(None))
async def approve_handler(
    message: Message,
    manager: DatabaseService,
) -> None:
    ready_users: list[tuple[User, int]] = await manager.get_users_with_answer_count()
    await message.answer("Ответы", reply_markup=AdminKeyboard.approves_keyboard(users=ready_users))


@router.callback_query(ApproveCallbackData.filter())
async def approve_cb_handler(
    query: CallbackQuery,
    manager: DatabaseService,
    callback_data: ApproveCallbackData,
) -> None:
    if isinstance(query.message, Message):
        ready_users: list[tuple[User, int]] = await manager.get_users_with_answer_count()
        await query.message.edit_text(
            "Ответы",
            reply_markup=AdminKeyboard.approves_keyboard(
                users=ready_users,
                current_page=callback_data.page,
            ),
        )


@router.callback_query(ApproveUserCallbackData.filter())
async def user_answers_callback_handler(
    query: CallbackQuery,
    manager: DatabaseService,
    callback_data: ApproveUserCallbackData,
) -> None:
    if isinstance(query.message, Message):
        user = await manager.get_user(callback_data.user_id)
        if user is None:
            return
        answers = await manager.get_user_unapproved_answers(callback_data.user_id)
        await query.message.edit_text(
            f"Ответы пользователя <b>{user.name}</b>",
            parse_mode="HTML",
            reply_markup=AdminKeyboard.user_unapproved_keyboard(
                answers=answers,
            ),
        )


@router.callback_query(AnswerCallbackData.filter())
async def answer_cb_handler(
    query: CallbackQuery,
    manager: DatabaseService,
    callback_data: AnswerCallbackData,
) -> None:
    if not isinstance(query.message, Message):
        return

    answers = await manager.get_answer(callback_data.answer_id)
    if answers is None:
        await query.answer("Ответ не найден", show_alert=True)
        return
    if not answers.videos:
        await query.answer("Ответ пустой", show_alert=True)
        return
    await query.message.reply_media_group(
        media=[InputMediaVideo(media=video.video_id) for video in answers.videos],
    )
    await query.message.answer(
        text=answers.chapter.name,
        reply_markup=AdminKeyboard.answer_keyboard(answers.id, answers.user_id),
    )
    await query.message.delete_reply_markup()


@router.callback_query(ApproveAnswerCallbackData.filter())
async def approve_answer_cb_handler(
    query: CallbackQuery,
    manager: DatabaseService,
    callback_data: ApproveAnswerCallbackData,
) -> None:
    if not isinstance(query.message, Message):
        return

    if callback_data.is_approved is True:
        await manager.approve_answer(callback_data.answer_id)
        await query.answer("✅ Ответ одобрен!")
    else:
        await manager.unapprove_answer(callback_data.answer_id)
        await query.answer("❌ Ответ отклонен!")

    await query.message.delete_reply_markup()
    await user_answers_callback_handler(
        query,
        manager,
        ApproveUserCallbackData(user_id=callback_data.user_id),
    )
