from typing import Self

from aiogram import Bot, Dispatcher
from loguru import logger

from src.config import Settings
from src.database import DatabaseService

from .services import admin_router, poll_router, registration_router


class Telegram:
    def __init__(self, token: str, settings: Settings) -> None:
        self._bot: Bot = Bot(token=token)
        self._dispatcher: Dispatcher = Dispatcher()
        self._settings: Settings = settings

    @classmethod
    def from_settings(cls, settings: Settings) -> Self:
        return cls(token=settings.TELEGRAM_TOKEN, settings=settings)

    async def start(self, manager: DatabaseService) -> None:
        logger.info("Starting telegram bot...")
        self._dispatcher.include_routers(
            registration_router,
            admin_router,
            poll_router,
        )
        await self._dispatcher.start_polling(self._bot, manager=manager, settings=self._settings)
