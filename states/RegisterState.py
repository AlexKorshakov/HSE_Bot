from aiogram.dispatcher.filters.state import StatesGroup, State


class RegisterState(StatesGroup):
    name = State()
    function = State()
    phone_number = State()
