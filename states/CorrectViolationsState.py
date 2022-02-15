from aiogram.dispatcher.filters.state import StatesGroup, State


class CorrectViolationsState(StatesGroup):
    description = State()
    comment = State()
    main_category = State()
    elimination_time = State()
    incident_level = State()
    act_required = State()
    general_constractor = State()
    category = State()
    violation_category = State()
