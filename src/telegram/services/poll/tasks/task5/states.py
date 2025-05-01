from aiogram.fsm.state import State, StatesGroup


class VideoT5StateGroup(StatesGroup):
    video = State()
