from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from src.config.resources import Form


def valid_answer(answer: str) -> bool:
    return bool(answer)


async def send(
    message: Message,
    form: Form,
    reply_button_text: str | None = None,
    callback_data: str | None = None,
) -> None:
    await message.delete_reply_markup()
    reply_keyboard: InlineKeyboardMarkup | None = None
    if reply_button_text is not None and callback_data is not None:
        reply_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=reply_button_text, callback_data=callback_data)],
            ],
        )
    if form.video_id is not None:
        await message.answer_video(
            caption=form.text,
            video=form.video_id,
            reply_markup=reply_keyboard,
        )
    else:
        await message.answer(
            text=form.text,
            reply_markup=reply_keyboard,
        )
