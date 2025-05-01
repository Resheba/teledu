from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.config import Texts

from .keyboards import EducationChapterCallbackData
from .tasks import start_task1, start_task2, start_task3

router: Router = Router(name="poll")


_starts = {
    1: start_task1,
    2: start_task2,
    3: start_task3,
}


@router.callback_query(EducationChapterCallbackData.filter(), StateFilter(None))
async def menu_cb_handler(
    query: CallbackQuery,
    callback_data: EducationChapterCallbackData,
    state: FSMContext,
    texts: Texts,
) -> None:
    if not isinstance(query.message, Message):
        return
    if callback_data.id not in _starts:
        return
    await _starts[callback_data.id](query.message, texts, state)
