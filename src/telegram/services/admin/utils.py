from dataclasses import dataclass
from typing import Literal

from aiogram import Bot
from aiogram.types import InputMediaVideo
from loguru import logger

from .keyboards import ApproveAnswerCallbackData, ExamApproveCallbackData


async def send_notification(
    bot: Bot,
    chat_id: int,
    message: str,
    media: list[InputMediaVideo] | None = None,
) -> None:
    try:
        await bot.send_message(chat_id=chat_id, text=message)
        if media:
            await bot.send_media_group(chat_id=chat_id, media=media)  # type: ignore[arg-type]
    except Exception as ex:  # noqa: BLE001
        logger.exception(ex)


@dataclass()
class Feedback:
    type: Literal["ANSWER", "EXAM"]
    callback_data: ApproveAnswerCallbackData | ExamApproveCallbackData
