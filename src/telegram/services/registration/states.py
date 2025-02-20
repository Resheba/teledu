from aiogram.fsm.state import State, StatesGroup


class RegistrationStateGroup(StatesGroup):
    name: State = State()
    email: State = State()
