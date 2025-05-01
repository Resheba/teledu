from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)

from src.config import Texts
from src.database import DatabaseService
from src.telegram.services.menu.router import menu_handler
from src.telegram.services.poll.states import TasksStateGroup
from src.telegram.services.poll.utils import send

from .keyboards import Task9CallbackData
from .states import VideoT9StateGroup

router: Router = Router(name="task9")


async def start(message: Message, texts: Texts, state: FSMContext) -> None:
    await state.set_state(TasksStateGroup.edu9)
    await send(
        message=message,
        form=texts.education.edu9.form_1,
        reply_button_text=texts.education.next_button_text,
        callback_data=Task9CallbackData(form=2).pack(),
    )


@router.callback_query(
    TasksStateGroup.edu9,
    Task9CallbackData.filter(F.form == 2),  # noqa: PLR2004
)
async def form2(
    query: CallbackQuery,
    callback_data: Task9CallbackData,
    texts: Texts,
) -> None:
    if not isinstance(query.message, Message):
        return
    await send(
        message=query.message,
        form=texts.education.edu9.form_2,
        reply_button_text=texts.education.next_button_text,
        callback_data=Task9CallbackData(form=callback_data.form + 1).pack(),
    )


@router.callback_query(
    TasksStateGroup.edu9,
    Task9CallbackData.filter(F.form == 3),  # noqa: PLR2004
)
async def form3(
    query: CallbackQuery,
    state: FSMContext,
    texts: Texts,
) -> None:
    if not isinstance(query.message, Message):
        return

    await query.message.answer(
        text=texts.education.edu9.form_3.text,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Отмена")],
            ],
            one_time_keyboard=True,
            resize_keyboard=True,
        ),
    )
    await state.set_state(VideoT9StateGroup.video)


@router.message(VideoT9StateGroup.video)
async def video(
    message: Message,
    state: FSMContext,
    texts: Texts,
) -> None:
    if message.text == "Отмена":
        await state.clear()
        await menu_handler(message=message)
        return
    if message.video is None:
        await message.answer("Пожалуйста, отправьте видео.")
        return
    await state.update_data(video=message.video.file_id)
    await state.set_state(TasksStateGroup.edu9)
    await message.answer(
        text="Видео сохранено!",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=texts.education.next_button_text,
                        callback_data=Task9CallbackData(form=4).pack(),
                    ),
                ],
            ],
        ),
    )


@router.callback_query(
    TasksStateGroup.edu9,
    Task9CallbackData.filter(F.form == 4),  # noqa: PLR2004
)
async def end(
    query: CallbackQuery,
    state: FSMContext,
    manager: DatabaseService,
) -> None:
    if not isinstance(query.message, Message):
        return
    await query.message.delete_reply_markup()
    data = await state.get_data()
    await state.clear()
    await manager.create_answer(
        user_id=query.message.chat.id,
        chapter_id=9,
        videos=[data["video"]],
    )
    await query.answer("Ответ сохранен!")
    await menu_handler(message=query.message)
