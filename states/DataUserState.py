from aiogram.dispatcher.filters.state import StatesGroup, State


class DataUserState(StatesGroup):

    user_data = State()
