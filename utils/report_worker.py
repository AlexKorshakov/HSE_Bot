from aiogram import types
from loguru import logger

from loader import bot
from messages.messages import Messages
from utils.generate_report.generator_report import create_report, create_report_from_other_method
from utils.generate_report.get_data_report import get_data_report
from utils.generate_report.get_file_list import get_json_file_list
from utils.generate_report.get_report_path import get_full_report_name

from utils.generate_report.send_report_from_user import send_report_from_user
from utils.set_user_report_data import set_report_data


async def create_and_send_report(message: types.Message):
    """Формирование и отправка отчета
    :param message:
    :return:
    """
    await message.answer(f'{Messages.report_start} \n'
                         f'{Messages.wait} \n'
                         f'{Messages.help_message}')

    file_list = await get_json_file_list(message)
    if not file_list:
        logger.warning('error! file_list not found!')
        await bot.send_message(message.from_user.id, Messages.file_list_not_found)

    dataframe = await get_data_report(message, file_list)
    if dataframe.empty:
        logger.warning('error! dataframe not found!')
        await message.answer(f"Не удалось получить данные для формирования отчета")

    full_report_path = await get_full_report_name(message)
    await create_report_from_other_method(message,
                                          dataframe=dataframe,
                                          full_report_path=full_report_path,
                                          file_list=file_list)

    # await create_report(message)

    await message.answer(f'{Messages.report_done} \n')

    # await set_report_data(message)

    await send_report_from_user(message, full_report_path=full_report_path)

    return True
