from typing import TYPE_CHECKING

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import CallbackQuery, Message

from src.database import DatabaseService

from .keyboards import AdminKeyboard, ApproveCallbackData, ApproveUserCallbackData

if TYPE_CHECKING:
    from src.database.models import User


router: Router = Router(name="admin")


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
        answers = await manager.get_user_chapter_answers(callback_data.user_id)
        await query.message.edit_text(
            f"Ответы пользователя <b>{user.name}</b>",
            parse_mode="HTML",
            reply_markup=AdminKeyboard.user_unapproved_keyboard(
                answer for answer in answers if answer.is_approved == "ON_ACC"
            ),
        )
