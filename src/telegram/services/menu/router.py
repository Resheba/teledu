from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.database import DatabaseService

from .keyboards import create_menu_keyboard

router: Router = Router(name="menu")


@router.message(Command("menu"))
async def menu_handler(
    message: Message,
    manager: DatabaseService,
) -> None:
    if message.from_user is None:  # bot check
        return
    user_tasks = await manager.get_user_tasks_statuses(message.from_user.id)
    await message.answer("Меню", reply_markup=create_menu_keyboard(user_tasks=user_tasks))
