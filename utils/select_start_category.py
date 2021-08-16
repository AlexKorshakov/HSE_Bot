from aiogram import types

from keyboards.inline.get_keyboard_fab import get_keyboard_fab


async def select_start_category(message: types.Message) -> None:
    """Действия при начале регистрации нарушения  / начале работы бота
    """
    await message.answer(text="Зарегистрировать нарушение?", reply_markup=get_keyboard_fab())