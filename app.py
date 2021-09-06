from __future__ import print_function
from aiogram import Dispatcher
from aiogram import executor

from data.config import SKIP_UPDATES, NUM_BUTTONS
from loguru import logger
from loader import dp, bot
from messages.messages import Messages

from utils.get_handled_updates_list import get_handled_updates_list

from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from utils.logger_config import setup_logger
from utils.shutdown import shutdown
from middlewares import setup_middlewares


async def on_startup(dispatcher: Dispatcher):
    setup_logger()
    logger.info("Установка обработчиков...")
    # Установка обработчиков производится посредством декораторов. Для этого достаточно просто импортировать модуль

    import filters
    import callbacks
    import handlers

    setup_middlewares(dispatcher)

    await on_startup_notify(dispatcher)
    await set_default_commands(dispatcher)
    logger.info(Messages.bot_start)


async def on_shutdown(dispatcher: Dispatcher):
    logger.warning('Bye! Shutting down connection')


if __name__ == '__main__':
    if NUM_BUTTONS in range(2, 8):
        try:
            executor.start_polling(dispatcher=dp,
                                   on_startup=on_startup,
                                   skip_updates=SKIP_UPDATES,
                                   on_shutdown=shutdown,
                                   allowed_updates=get_handled_updates_list(dp))
        finally:
            dp.storage.close()
            dp.storage.wait_closed()
            bot.session.close()
    else:
        raise AttributeError('количество кнопок не может быть меньше 2х или больше 7и')
