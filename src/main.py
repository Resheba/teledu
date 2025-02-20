import asyncio

from alchemynger import AsyncManager

from src.config import Settings

from .database import Base, DatabaseService
from .telegram import Telegram


async def main() -> None:
    manager: AsyncManager = AsyncManager(path="sqlite+aiosqlite:///test.sql", base=Base)
    await manager.create_all()

    db_service: DatabaseService = DatabaseService(manager=manager)

    settings: Settings = Settings.instance()
    telegram: Telegram = Telegram.from_settings(settings)
    await telegram.start(manager=db_service)


if __name__ == "__main__":
    asyncio.run(main())
