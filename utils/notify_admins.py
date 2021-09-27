from aiogram.utils.exceptions import ChatNotFound
from loguru import logger

from aiogram import Dispatcher
from asyncio import sleep

from data.config import ADMIN_ID


async def on_startup_notify(dp: Dispatcher):
    logger.info("Оповещение администрации...")
    # for admin_id in ADMINS_ID:
    try:
        await dp.bot.send_message(ADMIN_ID, "Бот был успешно запущен", disable_notification=True)
        logger.debug(f"Сообщение отправлено {ADMIN_ID}")
    except ChatNotFound:
        logger.debug("Чат с админом не найден")

    await sleep(0.3)