from aiogram import types

from keyboards.inline.get_keyboard_fab import get_keyboard_fab
from utils.del_messege import bot_delete_message


async def select_start_category(message: types.Message) -> None:
    """Действия при начале регистрации нарушения  / начале работы бота
    """
    markup= await get_keyboard_fab()

    await message.answer(text="Зарегистрировать нарушение?", reply_markup=markup)
    await bot_delete_message(chat_id=message.chat.id, message_id=message.message_id , sleep_time=20)
    await bot_delete_message(chat_id=message.chat.id, message_id=message.message_id + 1, sleep_time=20)
