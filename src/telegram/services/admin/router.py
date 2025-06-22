from typing import TYPE_CHECKING

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    InputMediaVideo,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)

from src.database import DatabaseService

from .filters import IsAdmin
from .keyboards import (
    AdminKeyboard,
    AnswerCallbackData,
    ApproveAnswerCallbackData,
    ApproveCallbackData,
    ApproveUserCallbackData,
    ExamApproveCallbackData,
    ExamCallbackData,
    ExamPageCallbackData,
)
from .states import FeedbackStateGroup
from .utils import Feedback, send_notification

if TYPE_CHECKING:
    from src.database.models import Answer, User


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
    callback_data: ApproveAnswerCallbackData,
    manager: DatabaseService,
    state: FSMContext,
) -> None:
    if not isinstance(query.message, Message) or (bot := query.bot) is None:
        return

    if callback_data.is_approved is False:
        await query.message.answer(
            "Оставьте комментарий",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="Отмена")],
                ],
                one_time_keyboard=True,
                resize_keyboard=True,
            ),
        )
        await state.set_state(FeedbackStateGroup.feedback)
        await state.update_data(feedback=Feedback(type="ANSWER", callback_data=callback_data))
    else:
        await query.answer("✅Ответ одобрен!")
        await manager.approve_answer(
            callback_data.answer_id,
        )
        await send_notification(
            bot=bot,
            chat_id=callback_data.user_id,
            message="✅Один из ответов был одобрен!",
        )

    await query.message.delete_reply_markup()


@router.callback_query(ExamPageCallbackData.filter())
async def exam_page_cb_handler(
    query: CallbackQuery,
    manager: DatabaseService,
    callback_data: ExamPageCallbackData,
) -> None:
    if not isinstance(query.message, Message):
        return
    exams = await manager.get_users_unapproved_exams()
    await query.message.edit_text(
        "Экзамены",
        reply_markup=AdminKeyboard.exams_keyboard(exams, current_page=callback_data.page),
    )


@router.message(Command("exams"), StateFilter(None))
async def exams_handler(
    message: Message,
    manager: DatabaseService,
) -> None:
    exams = await manager.get_users_unapproved_exams()
    await message.answer("Экзамены", reply_markup=AdminKeyboard.exams_keyboard(exams))


@router.callback_query(ExamApproveCallbackData.filter())
async def exam_approve_cb_handler(
    query: CallbackQuery,
    manager: DatabaseService,
    callback_data: ExamApproveCallbackData,
    state: FSMContext,
) -> None:
    if not isinstance(query.message, Message) or (bot := query.bot) is None:
        return

    if callback_data.is_approved is False:
        await query.message.answer(
            "Оставьте комментарий",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="Отмена")],
                ],
                one_time_keyboard=True,
                resize_keyboard=True,
            ),
        )
        await state.set_state(FeedbackStateGroup.feedback)
        await state.update_data(feedback=Feedback(type="EXAM", callback_data=callback_data))
    else:
        await query.answer("✅Экзамен одобрен!")
        await manager.mark_exam(
            callback_data.exam_id,
            mark=callback_data.is_approved,
        )
        await send_notification(
            bot=bot,
            chat_id=callback_data.user_id,
            message="✅ Экзамен одобрен!",
        )

    await query.message.delete_reply_markup()


@router.callback_query(ExamCallbackData.filter())
async def exam_cb_handler(
    query: CallbackQuery,
    manager: DatabaseService,
    callback_data: ExamCallbackData,
) -> None:
    if not isinstance(query.message, Message):
        return

    exam = await manager.get_exam(callback_data.exam_id)
    if exam is None:
        await query.answer("Ответ не найден", show_alert=True)
        return
    if not exam.video1_id or not exam.video2_id:
        await query.answer("Ответ пустой", show_alert=True)
        return
    await query.message.reply_media_group(
        media=[InputMediaVideo(media=exam.video1_id), InputMediaVideo(media=exam.video2_id)],
    )
    await query.message.answer(
        text=f"Экзамен <b>{callback_data.user_name}</b>",
        reply_markup=AdminKeyboard.exam_keyboard(exam.id, user_id=callback_data.user_id),
        parse_mode="HTML",
    )
    await query.message.delete_reply_markup()


@router.message(FeedbackStateGroup.feedback)
async def feedback_handler(
    message: Message,
    manager: DatabaseService,
    state: FSMContext,
) -> None:
    if message.text == "Отмена":
        await state.clear()
        await message.answer("Отменено")
        return
    feedback: Feedback | None = await state.get_value("feedback")
    if feedback is None:
        await state.clear()
        return
    if (bot := message.bot) is None:
        await state.clear()
        return
    if feedback.type == "ANSWER" and isinstance(feedback.callback_data, ApproveAnswerCallbackData):
        answer: Answer | None = await manager.get_answer(feedback.callback_data.answer_id)
        if feedback.callback_data.is_approved is True:
            await manager.approve_answer(feedback.callback_data.answer_id)
            await message.reply("✅ Ответ одобрен!")
        else:
            await manager.unapprove_answer(feedback.callback_data.answer_id)
            await message.reply("❌ Ответ отклонен!")
        await send_notification(
            bot=bot,
            chat_id=feedback.callback_data.user_id,
            message="✅ Ответ одобрен!"
            if feedback.callback_data.is_approved
            else f"❌ Ответ отклонен!\nКомменатрий:\n\n{message.text}",
            media=[InputMediaVideo(media=video.video_id) for video in answer.videos]
            if answer is not None
            else None,
        )
    elif feedback.type == "EXAM" and isinstance(feedback.callback_data, ExamApproveCallbackData):
        exam = await manager.get_exam(feedback.callback_data.exam_id)
        await manager.mark_exam(
            feedback.callback_data.exam_id,
            mark=feedback.callback_data.is_approved,
        )
        await message.reply(
            "✅ Экзамен одобрен!" if feedback.callback_data.is_approved else "❌ Экзамен отклонен!",
        )
        await send_notification(
            bot=bot,
            chat_id=feedback.callback_data.user_id,
            message="✅ Экзамен одобрен!"
            if feedback.callback_data.is_approved
            else f"❌ Экзамен отклонен!\nКомменатрий:\n\n{message.text}",
            media=[
                InputMediaVideo(media=exam.video1_id),
                InputMediaVideo(media=exam.video2_id),
            ]
            if exam is not None
            else None,
        )

    await state.clear()
