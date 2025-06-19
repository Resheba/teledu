from aiogram import Bot
from loguru import logger


async def send_notification(bot: Bot, chat_id: int, message: str) -> None:
    try:
        await bot.send_message(chat_id=chat_id, text=message)
    except Exception as ex:  # noqa: BLE001
        logger.exception(ex)
