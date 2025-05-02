from aiogram import Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from src.config import Texts
from src.database import DatabaseService

from .keyboards import (
    DocsCallbackData,
    EducationMenuCallbackData,
    LibraryCallbackData,
    MenuCallbackData,
    MenuKeyboard,
)

router: Router = Router(name="menu")


@router.message(Command("menu"))
async def menu_handler(
    message: Message,
    manager: DatabaseService | None = None,
) -> None:
    if manager is None:
        manager = DatabaseService.instance
    exam_status = await manager.get_exam_status(user_id=message.chat.id)
    await message.answer("Меню", reply_markup=MenuKeyboard.main_keyboard(exam_status=exam_status))


@router.callback_query(MenuCallbackData.filter())
async def menu_cb_handler(
    query: CallbackQuery,
    manager: DatabaseService,
) -> None:
    if isinstance(query.message, Message):
        exam_status = await manager.get_exam_status(user_id=query.message.chat.id)
        await query.message.edit_reply_markup(
            reply_markup=MenuKeyboard.main_keyboard(exam_status=exam_status),
        )


@router.callback_query(EducationMenuCallbackData.filter())
async def edu_handler(
    query: CallbackQuery,
    manager: DatabaseService,
) -> None:
    if isinstance(query.message, Message):
        answers = await manager.get_user_chapter_answers(query.message.chat.id)
        await query.message.edit_reply_markup(reply_markup=MenuKeyboard.edu_keyboard(answers))


@router.callback_query(LibraryCallbackData.filter())
async def library_handler(
    query: CallbackQuery,
    texts: Texts,
) -> None:
    if isinstance(query.message, Message):
        await query.message.edit_reply_markup(reply_markup=MenuKeyboard.library_keyboard(texts))


@router.callback_query(DocsCallbackData.filter())
async def docs_handler(
    query: CallbackQuery,
    callback_data: DocsCallbackData,
    texts: Texts,
) -> None:
    if isinstance(query.message, Message):
        await query.message.edit_reply_markup(
            reply_markup=MenuKeyboard.docs_keyboard(
                texts.documents.all[callback_data.page],
            ),
        )
