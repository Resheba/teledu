from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.config import Texts
from src.database import DatabaseService
from src.telegram.services.menu.router import menu_handler
from src.telegram.services.poll.states import TasksStateGroup
from src.telegram.services.poll.utils import send

from .keyboards import Task13CallbackData

router: Router = Router(name="task13")


async def start(
    message: Message,
    texts: Texts,
    state: FSMContext,
    manager: DatabaseService,
) -> None:
    if not (await manager.is_user_completed_all_chapters(message.chat.id)):
        await message.answer(
            "Вы не прошли все задания.\nПожалуйста, пройдите их или дождитесь проверки.",
        )
        return
    await state.set_state(TasksStateGroup.edu13)
    await send(
        message=message,
        form=texts.education.edu13.form_1,
        reply_button_text=texts.education.next_button_text,
        callback_data=Task13CallbackData(form=2).pack(),
    )


@router.callback_query(
    TasksStateGroup.edu13,
    Task13CallbackData.filter(F.form == 2),  # noqa: PLR2004
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
        chapter_id=13,
        videos=[],
    )
    await manager.approve_answer(answer.id)
    await query.answer("Ответ сохранен!")
    await menu_handler(message=query.message)
