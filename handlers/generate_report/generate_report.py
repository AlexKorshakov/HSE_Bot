from aiogram import types
from aiogram.dispatcher.filters import Command
from loguru import logger

from data.config import DEVELOPER_ID
from loader import dp
from messages.messages import Messages
from utils.misc import rate_limit
from utils.report_worker import create_and_send_mip_report
from utils.report_worker import create_and_send_report


@rate_limit(limit=10)
@dp.message_handler(Command('generate'))
async def generate(message: types.Message) -> None:
    """Формирование и отправка отчета пользователю
    :param message:
    :return: None
    """

    await message.answer(f'{Messages.Report.start} \n'
                         f'{Messages.wait}')

    # if message.chat.id == int(DEVELOPER_ID):
    logger.info(f'User @{message.from_user.username}:{message.from_user.id} generate mip report')
    if await create_and_send_mip_report(message):
        logger.info(Messages.Report.sent_successfully)

    logger.info(f'User @{message.from_user.username}:{message.from_user.id} generate report')
    if await create_and_send_report(message):
        logger.info(Messages.Report.sent_successfully)
