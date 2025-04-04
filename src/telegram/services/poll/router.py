# from asyncio import sleep as asleep

from aiogram import Router

# from aiogram.fsm.context import FSMContext
# from aiogram.types import InputMediaVideo, Message
# from loguru import logger

# from src.config import Settings, Texts
# from src.database import DatabaseService

# from .states import PollStateGroup
# from .utils import valid_answer

router: Router = Router(name="poll")


# async def start_poll(
#     message: Message,
#     settings: Settings,
#     state: FSMContext,
#     texts: Texts,
# ) -> None:
#     await message.answer(
#         "Я приготовил для тебе два видеоролика как надо безопасно работать на высоте на "
#         "опоре с использованием приставной лестницы. Их надо посмотреть.",
#     )
#     await asleep(1)
#     await message.answer(
#         "После просмотра роликов я попрошу тебя пошагово повторить и записать "
#         "видео как ты это делаешь. Я помогу тебе. У нас все получиться.",
#     )
#     await asleep(1)
#     await message.answer_media_group(
#         media=[InputMediaVideo(media=media_id) for media_id in settings.VIDEO_IDS],
#     )
#     await state.set_state(PollStateGroup.overview)
#     await asleep(1)
#     await message.answer(
#         "Теперь давайте повторим пройденный материал. "
#         "Пожалуйста, напишите, что вы поняли из видео.",
#     )


# @router.message(PollStateGroup.overview)
# async def poll_overview(message: Message, state: FSMContext) -> None:
#     if not message.text or not valid_answer(message.text or ""):
#         await message.answer("Пожалуйста, напишите, что вы поняли из видео.")
#         return
#     await state.update_data(text_answer=message.text)
#     await message.answer("Отлично! Теперь попробуйте выполнить следующее задание.")
#     await asleep(1)
#     await message.answer("Запишите видео с вашим исполнением задания.")
#     await state.set_state(PollStateGroup.video)


# @router.message(PollStateGroup.video, F.video | F.text)
# async def poll_video(message: Message, state: FSMContext, manager: DatabaseService) -> None:
#     if message.from_user is None:  # bot check
#         await state.clear()
#         return
#     if not message.video:
#         await message.answer("Пожалуйста, отправьте видео.")
#         return
#     await manager.create_answer(
#         user_id=message.from_user.id,
#         text_answer=await state.get_value("text_answer", ""),
#         video_answer_id=message.video.file_id,
#     )
#     logger.info(f"User {message.from_user.id} completed poll.")
#     await message.answer("Ваша работа отправлена на проверку! Мы свяжемся с вами скоро.")
#     await state.clear()
