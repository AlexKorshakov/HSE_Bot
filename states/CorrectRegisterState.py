from aiogram.dispatcher.filters.state import StatesGroup, State


class CorrectRegisterState(StatesGroup):
    name = State()
    function = State()
    phone_number = State()
    work_shift = State()
    name_location = State()
