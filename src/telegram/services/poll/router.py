from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.config import Texts
from src.database import DatabaseService

from .keyboards import EducationChapterCallbackData
from .tasks import (
    start_task1,
    start_task2,
    start_task3,
    start_task4,
    start_task5,
    start_task6,
    start_task7,
    start_task8,
    start_task9,
    start_task10,
    start_task11,
    start_task12,
)

router: Router = Router(name="poll")


_starts = {
    1: start_task1,
    2: start_task2,
    3: start_task3,
    4: start_task4,
    5: start_task5,
    6: start_task6,
    7: start_task7,
    8: start_task8,
    9: start_task9,
    10: start_task10,
    11: start_task11,
}


@router.callback_query(EducationChapterCallbackData.filter(), StateFilter(None))
async def menu_cb_handler(
    query: CallbackQuery,
    callback_data: EducationChapterCallbackData,
    state: FSMContext,
    manager: DatabaseService,
    texts: Texts,
) -> None:
    if not isinstance(query.message, Message):
        return
    if callback_data.id == 12:  # noqa: PLR2004
        await start_task12(query.message, texts, state, manager)
        return
    if callback_data.id not in _starts:
        return
    await _starts[callback_data.id](query.message, texts, state)
