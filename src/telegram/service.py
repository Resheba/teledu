from typing import Self

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from loguru import logger

from src.config import Settings, Texts
from src.database import DatabaseService

from .services import (
    admin_router,
    exam_router,
    poll_router,
    registration_router,
    task1_router,
    task2_router,
    task3_router,
    task4_router,
    task5_router,
    task6_router,
    task7_router,
    task8_router,
    task9_router,
    task10_router,
    task11_router,
    task12_router,
    task13_router,
)
from .services.menu.router import router as menu_router


class Telegram:
    def __init__(self, token: str, settings: Settings) -> None:
        self._bot: Bot = Bot(token=token)
        self._dispatcher: Dispatcher = Dispatcher()
        self._settings: Settings = settings

    @classmethod
    def from_settings(cls, settings: Settings) -> Self:
        return cls(token=settings.TELEGRAM_TOKEN, settings=settings)

    async def start(self, manager: DatabaseService, texts: Texts) -> None:
        logger.info("Starting telegram bot...")
        self._dispatcher.include_routers(
            registration_router,
            admin_router,
            poll_router,
            menu_router,
            task1_router,
            task2_router,
            task3_router,
            task4_router,
            task5_router,
            task6_router,
            task7_router,
            task8_router,
            task9_router,
            task10_router,
            task11_router,
            task12_router,
            task13_router,
            exam_router,
        )
        await self._bot.set_my_commands(
            commands=[
                BotCommand(command="/start", description="Start"),
                BotCommand(command="/menu", description="Menu"),
                BotCommand(command="/approves", description="Approves"),
                BotCommand(command="/exams", description="Exams"),
            ],
        )
        await self._dispatcher.start_polling(
            self._bot,
            manager=manager,
            settings=self._settings,
            texts=texts,
        )
