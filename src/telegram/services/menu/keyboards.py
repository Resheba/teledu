from collections.abc import Iterable

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.database.models import Task


def _status_to_icon(status: bool | None) -> str:
    if status is None:
        return ""
    return "✅" if status else "❌"


def create_menu_keyboard(user_tasks: Iterable[tuple[Task, bool | None]]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{_status_to_icon(status)} {task.name}".strip(),
                    callback_data="ABOBA",
                ),
            ]
            for task, status in user_tasks
            if task.name
        ],
    )
