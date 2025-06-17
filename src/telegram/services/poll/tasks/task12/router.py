from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.config import Texts
from src.database import DatabaseService
from src.telegram.services.menu.router import menu_handler
from src.telegram.services.poll.states import TasksStateGroup
from src.telegram.services.poll.utils import send

from .keyboards import Task12CallbackData

router: Router = Router(name="task12")


async def start(
    message: Message,
    texts: Texts,
    state: FSMContext,
) -> None:
    await state.set_state(TasksStateGroup.edu12)
    await send(
        message=message,
        form=texts.education.edu12.form_1,
        reply_button_text=texts.education.next_button_text,
        callback_data=Task12CallbackData(form=2).pack(),
    )


@router.callback_query(
    TasksStateGroup.edu12,
    Task12CallbackData.filter(F.form == 2),  # noqa: PLR2004
)
async def form2(
    query: CallbackQuery,
    callback_data: Task12CallbackData,
    texts: Texts,
) -> None:
    if not isinstance(query.message, Message):
        return
    await send(
        message=query.message,
        form=texts.education.edu12.form_2,
        reply_button_text=texts.education.next_button_text,
        callback_data=Task12CallbackData(form=callback_data.form + 1).pack(),
    )


@router.callback_query(
    TasksStateGroup.edu12,
    Task12CallbackData.filter(F.form == 3),  # noqa: PLR2004
)
async def form3(
    query: CallbackQuery,
    callback_data: Task12CallbackData,
    texts: Texts,
) -> None:
    if not isinstance(query.message, Message):
        return
    await send(
        message=query.message,
        form=texts.education.edu12.form_3,
        reply_button_text=texts.education.next_button_text,
        callback_data=Task12CallbackData(form=callback_data.form + 1).pack(),
    )


@router.callback_query(
    TasksStateGroup.edu12,
    Task12CallbackData.filter(F.form == 4),  # noqa: PLR2004
)
async def end(
    query: CallbackQuery,
    state: FSMContext,
    manager: DatabaseService,
) -> None:
    if not isinstance(query.message, Message):
        return
    await query.message.delete_reply_markup()
    await state.clear()
    answer = await manager.create_answer(
        user_id=query.message.chat.id,
        chapter_id=12,
        videos=[],
    )
    await manager.approve_answer(answer.id)
    await query.answer("Ответ сохранен!")
    await menu_handler(message=query.message)
