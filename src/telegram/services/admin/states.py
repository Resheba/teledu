from aiogram.fsm.state import State, StatesGroup


class FeedbackStateGroup(StatesGroup):
    feedback = State()
