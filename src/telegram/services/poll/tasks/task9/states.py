from aiogram.fsm.state import State, StatesGroup


class VideoT9StateGroup(StatesGroup):
    video = State()
