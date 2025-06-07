from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message

from src.config import Settings


class IsAdmin(BaseFilter):
    _admin_id = Settings.instance().ADMIN_IDS

    async def __call__(self, message: Message) -> bool:
        if isinstance(message, CallbackQuery) and message.message is not None:
            message = message.message
        return message.chat.id in self._admin_id
