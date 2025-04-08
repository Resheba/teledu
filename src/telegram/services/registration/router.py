from asyncio import sleep

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from loguru import logger

from src.config import Texts
from src.database import DatabaseService
from src.telegram.services.menu.router import menu_handler

from .states import RegistrationStateGroup
from .utils import valid_email, valid_name, valid_number

router: Router = Router(name="registration")


@router.message(CommandStart())
async def start_command(
    message: Message,
    state: FSMContext,
    manager: DatabaseService,
    texts: Texts,
) -> None:
    await message.answer_photo(texts.registration.image_id, caption=texts.registration.form_1.text)
    if not await manager.is_user_created(message.chat.id):
        await state.set_state(RegistrationStateGroup.name)
        await message.answer(texts.registration.form_2.text)
    else:
        await sleep(0.8)
        await menu_handler(message=message)


@router.message(RegistrationStateGroup.name)
async def reg_name(
    message: Message,
    state: FSMContext,
    texts: Texts,
) -> None:
    if message.text and valid_name(name := message.text.strip()):
        await state.update_data(name=name)
        await message.reply(f"Приятно познакомиться, {name}!")
        await state.set_state(RegistrationStateGroup.email)
        await message.answer(texts.registration.form_3.text)
    else:
        await message.answer("Некорректное имя.\nПожалуйста, введите Ваше имя.")


@router.message(RegistrationStateGroup.email)
async def reg_email(
    message: Message,
    state: FSMContext,
    manager: DatabaseService,
    texts: Texts,
) -> None:
    if message.from_user is None:  # bot check
        await state.clear()
        return
    if message.text and (valid_email(email := message.text.strip()) or valid_number(number=email)):
        await message.answer(texts.registration.form_4.text)
        await manager.create_user(
            user_id=message.from_user.id,
            contact=email,
            name=await state.get_value("name", ""),
        )
        await state.clear()
        logger.info(f"User {message.from_user.id} registered.")
        await menu_handler(message=message)
    else:
        await message.answer("Некорректные данные, повторите попытку.")
