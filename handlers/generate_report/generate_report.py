from aiogram import types
from aiogram.dispatcher.filters import Command
from loguru import logger

from loader import dp
from utils.misc import rate_limit
from utils.report_worker import create_and_send_report


@rate_limit(limit=10)
@dp.message_handler(Command('generate'))
async def generate(message: types.Message) -> None:
    """Формирование и отправка отчета пользователю
    :param message:
    :return: None
    """
    logger.info(f'User @{message.from_user.username}:{message.from_user.id} generate report')
    if await create_and_send_report(message):
        logger.info(f'Отчет успешно отправлен!')
