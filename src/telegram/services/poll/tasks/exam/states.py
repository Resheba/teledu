from aiogram.fsm.state import State, StatesGroup


class VideoExamStateGroup(StatesGroup):
    video1 = State()
    video2 = State()
