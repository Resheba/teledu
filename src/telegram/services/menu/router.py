from aiogram import Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from src.config import Texts

from .keyboards import EducationMenuCallbackData, MenuCallbackData, MenuKeyboard

router: Router = Router(name="menu")


@router.message(Command("menu"))
async def menu_handler(
    message: Message,
) -> None:
    await message.answer("Меню", reply_markup=MenuKeyboard.main_keyboard)


@router.callback_query(MenuCallbackData.filter())
async def menu_cb_handler(
    query: CallbackQuery,
) -> None:
    if isinstance(query.message, Message):
        await query.message.edit_reply_markup(reply_markup=MenuKeyboard.main_keyboard)


@router.callback_query(EducationMenuCallbackData.filter())
async def edu_handler(
    query: CallbackQuery,
    texts: Texts,
) -> None:
    if isinstance(query.message, Message):
        await query.message.edit_reply_markup(reply_markup=MenuKeyboard.edu_keyboard(texts))
