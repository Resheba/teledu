from typing import Self

from aiogram import Bot, Dispatcher
from loguru import logger

from src.config import Settings

from .services import registration_router


class Telegram:
    def __init__(self, token: str) -> None:
        self._bot: Bot = Bot(token=token)
        self._dispatcher: Dispatcher = Dispatcher()

    @classmethod
    def from_settings(cls, settings: Settings) -> Self:
        return cls(token=settings.TELEGRAM_TOKEN)

    async def start(self) -> None:
        logger.info("Starting telegram bot...")
        self._dispatcher.include_routers(registration_router)
        await self._dispatcher.start_polling(self._bot)
