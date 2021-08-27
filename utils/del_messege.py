import asyncio
from contextlib import suppress

from aiogram.utils.exceptions import (MessageToEditNotFound, MessageCantBeEdited, MessageCantBeDeleted,
                                      MessageToDeleteNotFound)

from data.config import BOT_DELETE_MESSAGE
from loader import bot


async def bot_delete_message(chat_id: str, message_id: str, sleep_time: int = 1):
    """Удаление сообщений по таймеру
    :param message_id: id сообщения
    :param chat_id: id чата из которого удаляется сообщение
    :param sleep_time:int - время в секундах
    :return:
    """
    if BOT_DELETE_MESSAGE:
        await asyncio.sleep(sleep_time)
        with suppress(MessageToEditNotFound, MessageCantBeEdited, MessageCantBeDeleted, MessageToDeleteNotFound):
            await bot.delete_message(chat_id=chat_id, message_id=message_id)
