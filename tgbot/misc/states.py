from aiogram.dispatcher.filters.state import StatesGroup, State


class UsersStates(StatesGroup):
    round_counter = State()
