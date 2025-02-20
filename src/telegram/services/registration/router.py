from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from loguru import logger

from .states import RegistrationStateGroup
from .utils import valid_email, valid_name

router: Router = Router(name="registration")


@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext) -> None:
    # TODO: if user is not registered, show registration form
    if message.from_user is None:  # bot check
        return
    await message.answer(
        "Привет! Это чат-бот для обучения безопасности работ на опорах "
        "воздушных линиях связи с использованием приставных лестниц!",
    )
    if message.from_user.id:  # reg check
        await state.set_state(RegistrationStateGroup.name)
        await message.answer("Как вас зовут?")


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
async def reg_email(message: Message, state: FSMContext) -> None:
    if message.text and valid_email(email := message.text.strip()):
        await state.update_data(email=email)
        await message.answer("Вы успешно зарегистрированы!")
        logger.info(await state.get_data())
    else:
        await message.answer("Некорректный email.\nПожалуйста, введите Ваш email.")
