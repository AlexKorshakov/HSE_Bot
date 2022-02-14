from aiogram.dispatcher.filters.state import StatesGroup, State


class CorrectHeadlinesState(StatesGroup):
    construction_manager = State()
    building_control_engineer = State()
    general_contractor = State()
    subcontractor = State()
    name_location = State()
    linear_bypass = State()
    date_linear_bypass = State()
    contractor_representative = State()
    subcontractor_representative = State()
