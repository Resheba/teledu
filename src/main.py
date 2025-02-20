import asyncio

from src.config import Settings

from .telegram import Telegram


async def main() -> None:
    settings: Settings = Settings.instance()
    await Telegram.from_settings(settings).start()


if __name__ == "__main__":
    asyncio.run(main())
