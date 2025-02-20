from aiogram.fsm.state import State, StatesGroup


class PollStateGroup(StatesGroup):
    overview: State = State()
    video: State = State()
