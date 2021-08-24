import asyncio
from contextlib import suppress

from aiogram import types
from aiogram.utils.exceptions import (MessageToEditNotFound, MessageCantBeEdited, MessageCantBeDeleted,
                                      MessageToDeleteNotFound)

from loader import bot


async def _delete_message(message: types.Message, sleep_time: int = 0):
    await asyncio.sleep(sleep_time)
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await message.delete()


# msg = await message.reply("Я удалюсь через 30 секунд")
# asyncio.create_task(_delete_message(msg, 30))


async def bot_delete_message(chat_id, message_id, sleep_time: int = 1):
    await asyncio.sleep(sleep_time)
    with suppress(MessageToEditNotFound, MessageCantBeEdited, MessageCantBeDeleted, MessageToDeleteNotFound):
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
