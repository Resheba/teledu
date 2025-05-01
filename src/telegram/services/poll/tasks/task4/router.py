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

from .keyboards import Task4CallbackData
from .states import VideoT4StateGroup

router: Router = Router(name="task4")


async def start(message: Message, texts: Texts, state: FSMContext) -> None:
    await state.set_state(TasksStateGroup.edu4)
    await send(
        message=message,
        form=texts.education.edu4.form_1,
        reply_button_text=texts.education.next_button_text,
        callback_data=Task4CallbackData(form=2).pack(),
    )


@router.callback_query(
    TasksStateGroup.edu4,
    Task4CallbackData.filter(F.form == 2),  # noqa: PLR2004
)
async def form2(
    query: CallbackQuery,
    callback_data: Task4CallbackData,
    texts: Texts,
) -> None:
    if not isinstance(query.message, Message):
        return
    await send(
        message=query.message,
        form=texts.education.edu4.form_2,
        reply_button_text=texts.education.next_button_text,
        callback_data=Task4CallbackData(form=callback_data.form + 1).pack(),
    )


@router.callback_query(
    TasksStateGroup.edu4,
    Task4CallbackData.filter(F.form == 3),  # noqa: PLR2004
)
async def form3(
    query: CallbackQuery,
    callback_data: Task4CallbackData,
    texts: Texts,
) -> None:
    if not isinstance(query.message, Message):
        return
    await send(
        message=query.message,
        form=texts.education.edu4.form_3,
        reply_button_text=texts.education.next_button_text,
        callback_data=Task4CallbackData(form=callback_data.form + 1).pack(),
    )


@router.callback_query(
    TasksStateGroup.edu4,
    Task4CallbackData.filter(F.form == 4),  # noqa: PLR2004
)
async def form4(
    query: CallbackQuery,
    state: FSMContext,
    texts: Texts,
) -> None:
    if not isinstance(query.message, Message):
        return

    await query.message.answer(
        text=texts.education.edu4.form_4.text,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Отмена")],
            ],
            one_time_keyboard=True,
            resize_keyboard=True,
        ),
    )
    await state.set_state(VideoT4StateGroup.video1)


@router.message(VideoT4StateGroup.video1)
async def video1(
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
    await state.update_data(video1=message.video.file_id)
    await state.set_state(TasksStateGroup.edu4)
    await message.answer(
        text="Видео сохранено!",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=texts.education.next_button_text,
                        callback_data=Task4CallbackData(form=5).pack(),
                    ),
                ],
            ],
        ),
    )


@router.callback_query(
    TasksStateGroup.edu4,
    Task4CallbackData.filter(F.form == 5),  # noqa: PLR2004
)
async def form5(
    query: CallbackQuery,
    callback_data: Task4CallbackData,
    texts: Texts,
) -> None:
    if not isinstance(query.message, Message):
        return
    await send(
        message=query.message,
        form=texts.education.edu4.form_5,
        reply_button_text=texts.education.next_button_text,
        callback_data=Task4CallbackData(form=callback_data.form + 1).pack(),
    )


@router.callback_query(
    TasksStateGroup.edu4,
    Task4CallbackData.filter(F.form == 6),  # noqa: PLR2004
)
async def form6(
    query: CallbackQuery,
    callback_data: Task4CallbackData,
    texts: Texts,
) -> None:
    if not isinstance(query.message, Message):
        return
    await send(
        message=query.message,
        form=texts.education.edu4.form_6,
        reply_button_text=texts.education.next_button_text,
        callback_data=Task4CallbackData(form=callback_data.form + 1).pack(),
    )


@router.callback_query(
    TasksStateGroup.edu4,
    Task4CallbackData.filter(F.form == 7),  # noqa: PLR2004
)
async def form7(
    query: CallbackQuery,
    state: FSMContext,
    texts: Texts,
) -> None:
    if not isinstance(query.message, Message):
        return

    await query.message.answer(
        text=texts.education.edu4.form_7.text,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Отмена")],
            ],
            one_time_keyboard=True,
            resize_keyboard=True,
        ),
    )
    await state.set_state(VideoT4StateGroup.video2)


@router.message(VideoT4StateGroup.video2)
async def video2(
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
    await state.update_data(video2=message.video.file_id)
    await state.set_state(TasksStateGroup.edu4)
    await message.answer(
        text="Видео сохранено!",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=texts.education.next_button_text,
                        callback_data=Task4CallbackData(form=8).pack(),
                    ),
                ],
            ],
        ),
    )


@router.callback_query(
    TasksStateGroup.edu4,
    Task4CallbackData.filter(F.form == 8),  # noqa: PLR2004
)
async def form8(
    query: CallbackQuery,
    callback_data: Task4CallbackData,
    texts: Texts,
) -> None:
    if not isinstance(query.message, Message):
        return
    await send(
        message=query.message,
        form=texts.education.edu4.form_8,
        reply_button_text=texts.education.next_button_text,
        callback_data=Task4CallbackData(form=callback_data.form + 1).pack(),
    )


@router.callback_query(
    TasksStateGroup.edu4,
    Task4CallbackData.filter(F.form == 9),  # noqa: PLR2004
)
async def form9(
    query: CallbackQuery,
    callback_data: Task4CallbackData,
    texts: Texts,
) -> None:
    if not isinstance(query.message, Message):
        return
    await send(
        message=query.message,
        form=texts.education.edu4.form_9,
        reply_button_text=texts.education.next_button_text,
        callback_data=Task4CallbackData(form=callback_data.form + 1).pack(),
    )


@router.callback_query(
    TasksStateGroup.edu4,
    Task4CallbackData.filter(F.form == 10),  # noqa: PLR2004
)
async def form10(
    query: CallbackQuery,
    state: FSMContext,
    texts: Texts,
) -> None:
    if not isinstance(query.message, Message):
        return

    await query.message.answer(
        text=texts.education.edu4.form_10.text,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Отмена")],
            ],
            one_time_keyboard=True,
            resize_keyboard=True,
        ),
    )
    await state.set_state(VideoT4StateGroup.video3)


@router.message(VideoT4StateGroup.video3)
async def video3(
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
    await state.update_data(video3=message.video.file_id)
    await state.set_state(TasksStateGroup.edu4)
    await message.answer(
        text="Видео сохранено!",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=texts.education.next_button_text,
                        callback_data=Task4CallbackData(form=11).pack(),
                    ),
                ],
            ],
        ),
    )


@router.callback_query(
    TasksStateGroup.edu4,
    Task4CallbackData.filter(F.form == 11),  # noqa: PLR2004
)
async def form11(
    query: CallbackQuery,
    callback_data: Task4CallbackData,
    texts: Texts,
) -> None:
    if not isinstance(query.message, Message):
        return
    await send(
        message=query.message,
        form=texts.education.edu4.form_11,
        reply_button_text=texts.education.next_button_text,
        callback_data=Task4CallbackData(form=callback_data.form + 1).pack(),
    )


@router.callback_query(
    TasksStateGroup.edu4,
    Task4CallbackData.filter(F.form == 12),  # noqa: PLR2004
)
async def form12(
    query: CallbackQuery,
    callback_data: Task4CallbackData,
    texts: Texts,
) -> None:
    if not isinstance(query.message, Message):
        return
    await send(
        message=query.message,
        form=texts.education.edu4.form_12,
        reply_button_text=texts.education.next_button_text,
        callback_data=Task4CallbackData(form=callback_data.form + 1).pack(),
    )


@router.callback_query(
    TasksStateGroup.edu4,
    Task4CallbackData.filter(F.form == 13),  # noqa: PLR2004
)
async def form13(
    query: CallbackQuery,
    state: FSMContext,
    texts: Texts,
) -> None:
    if not isinstance(query.message, Message):
        return

    await query.message.answer(
        text=texts.education.edu4.form_13.text,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Отмена")],
            ],
            one_time_keyboard=True,
            resize_keyboard=True,
        ),
    )
    await state.set_state(VideoT4StateGroup.video4)


@router.message(VideoT4StateGroup.video4)
async def video4(
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
    await state.update_data(video4=message.video.file_id)
    await state.set_state(TasksStateGroup.edu4)
    await message.answer(
        text="Видео сохранено!",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=texts.education.next_button_text,
                        callback_data=Task4CallbackData(form=14).pack(),
                    ),
                ],
            ],
        ),
    )


@router.callback_query(
    TasksStateGroup.edu4,
    Task4CallbackData.filter(F.form == 14),  # noqa: PLR2004
)
async def form14(
    query: CallbackQuery,
    callback_data: Task4CallbackData,
    texts: Texts,
) -> None:
    if not isinstance(query.message, Message):
        return
    await send(
        message=query.message,
        form=texts.education.edu4.form_14,
        reply_button_text=texts.education.next_button_text,
        callback_data=Task4CallbackData(form=callback_data.form + 1).pack(),
    )


@router.callback_query(
    TasksStateGroup.edu4,
    Task4CallbackData.filter(F.form == 15),  # noqa: PLR2004
)
async def form15(
    query: CallbackQuery,
    callback_data: Task4CallbackData,
    texts: Texts,
) -> None:
    if not isinstance(query.message, Message):
        return
    await send(
        message=query.message,
        form=texts.education.edu4.form_15,
        reply_button_text=texts.education.next_button_text,
        callback_data=Task4CallbackData(form=callback_data.form + 1).pack(),
    )


@router.callback_query(
    TasksStateGroup.edu4,
    Task4CallbackData.filter(F.form == 16),  # noqa: PLR2004
)
async def form16(
    query: CallbackQuery,
    state: FSMContext,
    texts: Texts,
) -> None:
    if not isinstance(query.message, Message):
        return

    await query.message.answer(
        text=texts.education.edu4.form_16.text,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Отмена")],
            ],
            one_time_keyboard=True,
            resize_keyboard=True,
        ),
    )
    await state.set_state(VideoT4StateGroup.video5)


@router.message(VideoT4StateGroup.video5)
async def video5(
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
    await state.update_data(video5=message.video.file_id)
    await state.set_state(TasksStateGroup.edu4)
    await message.answer(
        text="Видео сохранено!",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=texts.education.next_button_text,
                        callback_data=Task4CallbackData(form=17).pack(),
                    ),
                ],
            ],
        ),
    )


@router.callback_query(
    TasksStateGroup.edu4,
    Task4CallbackData.filter(F.form == 17),  # noqa: PLR2004
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
        chapter_id=4,
        videos=[data["video1"], data["video2"], data["video3"], data["video4"], data["video5"]],
    )
    await query.answer("Ответ сохранен!")
    await menu_handler(message=query.message)
