from aiogram.dispatcher.filters.state import StatesGroup, State


class TestState(StatesGroup):
    somelist = State()
    level = State()
