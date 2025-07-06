import asyncio
from pathlib import Path

from alchemynger import AsyncManager
from sqlalchemy import text

from src.config import Settings, Texts

from .database import Base, DatabaseService
from .telegram import Telegram
from .utils import sorted_chapters


async def main() -> None:
    settings: Settings = Settings.instance()
    _texts_path: Path = Path(settings.TEXTS_PATH)
    if not _texts_path.exists():
        raise FileNotFoundError(f"File {_texts_path} not found. Please, read README.md")
    texts: Texts = Texts.model_validate_json(_texts_path.read_text(encoding="utf-8"))

    manager: AsyncManager = AsyncManager(path="sqlite+aiosqlite:///base.sql", base=Base)
    await manager.execute(text("PRAGMA foreign_keys=ON"))  # fix sqlite fk cascade
    await manager.create_all()

    db_service: DatabaseService = DatabaseService(manager=manager)
    DatabaseService.instance = db_service
    await db_service.migrate_chapters(
        chapters_names=sorted_chapters(texts),
    )

    telegram: Telegram = Telegram.from_settings(settings)
    await telegram.start(manager=db_service, texts=texts)


if __name__ == "__main__":
    asyncio.run(main())
