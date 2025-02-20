from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from loguru import logger

from src.config import Settings
from src.database import DatabaseService
from src.telegram.services.poll.router import start_poll

from .states import RegistrationStateGroup
from .utils import valid_email, valid_name

router: Router = Router(name="registration")


@router.message(CommandStart())
async def start_command(
    message: Message,
    state: FSMContext,
    manager: DatabaseService,
    settings: Settings,
) -> None:
    if message.from_user is None:  # bot check
        return
    await message.answer(
        "Привет! Это чат-бот для обучения безопасности работ на опорах "
        "воздушных линиях связи с использованием приставных лестниц!",
    )
    if not await manager.is_user_created(message.from_user.id):
        await state.set_state(RegistrationStateGroup.name)
        await message.answer("Как вас зовут?")
    else:
        await start_poll(message=message, settings=settings, state=state)


@router.message(RegistrationStateGroup.name)
async def reg_name(message: Message, state: FSMContext) -> None:
    if message.text and valid_name(name := message.text.strip()):
        await state.update_data(name=name)
        await message.reply(f"Приятно познакомиться, {name}!")
        await state.set_state(RegistrationStateGroup.email)
        await message.answer("Пожалуйста, зарегистрируйтесь, указав свою электронную почту.")
    else:
        await message.answer("Некорректное имя.\nПожалуйста, введите Ваше имя.")


@router.message(RegistrationStateGroup.email)
async def reg_email(
    message: Message,
    state: FSMContext,
    manager: DatabaseService,
    settings: Settings,
) -> None:
    if message.from_user is None:  # bot check
        await state.clear()
        return
    if message.text and valid_email(email := message.text.strip()):
        await message.answer("Вы успешно зарегистрированы!")
        await manager.create_user(
            user_id=message.from_user.id,
            email=email,
            name=await state.get_value("name", ""),
        )
        await state.clear()
        logger.info(f"User {message.from_user.id} registered.")
        await start_poll(message=message, settings=settings, state=state)
    else:
        await message.answer("Некорректный email.\nПожалуйста, введите Ваш email.")
