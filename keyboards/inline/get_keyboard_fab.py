from aiogram import types

from callbacks.callback_action import cb_start


async def get_keyboard_fab():
    """Действия при начале регистрации нарушений.
    ВОзвращает кнопри Зарегистрировать и Отмена
    """
    buttons = [
        types.InlineKeyboardButton(text="Зарегистрировать", callback_data=cb_start.new(action="start_registration")),
        types.InlineKeyboardButton(text="Отмена", callback_data=cb_start.new(action="abort_registration"))
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard