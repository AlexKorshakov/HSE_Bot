from aiogram import types
from loguru import logger

from loader import bot
from messages.messages import Messages
from utils.generate_report.generator_report import create_report_from_other_method, create_mip_report
from utils.generate_report.get_data_report import get_data_report
from utils.generate_report.get_file_list import get_json_file_list, get_registration_json_file_list
from utils.generate_report.get_report_path import get_full_report_name, get_full_mip_report_name
from utils.generate_report.send_report_from_user import send_report_from_user
from utils.json_worker.read_json_file import read_json_file
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
        logger.warning(Messages.error_file_list_not_found)
        await bot.send_message(message.from_user.id, Messages.error_file_list_not_found)

    dataframe = await get_data_report(message, file_list)
    if dataframe.empty:
        logger.warning(Messages.error_dataframe_not_found)
        await message.answer(Messages.error_dataframe_not_found)

    full_report_path = await get_full_report_name(message)
    await create_report_from_other_method(message,
                                          dataframe=dataframe,
                                          full_report_path=full_report_path,
                                          file_list=file_list)

    await message.answer(f'{Messages.report_done} \n')

    await set_report_data(message, full_report_path)

    await send_report_from_user(message, full_report_path=full_report_path)

    return True


async def create_and_send_mip_report(message: types.Message):
    """Формирование и отправка отчета
    :param message:
    :return:
    """
    # await message.answer(f'{Messages.report_start} \n'
    #                      f'{Messages.wait} \n'
    #                      f'{Messages.help_message}')

    file_list = await get_json_file_list(message)
    if not file_list:
        logger.warning(Messages.error_file_list_not_found)
        await bot.send_message(message.from_user.id, Messages.error_file_list_not_found)

    registration_file_list = await get_registration_json_file_list(chat_id=message.chat.id)
    if not registration_file_list:
        logger.warning(Messages.error_registration_file_list_not_found)
        await bot.send_message(message.from_user.id, Messages.error_file_list_not_found)

    # dataframe = await get_data_report(message, file_list)
    # if dataframe.empty:
    #     logger.warning('error! dataframe not found!')
    #     await message.answer(f"Не удалось получить данные для формирования отчета")

    registration_data = await read_json_file(registration_file_list)
    location_name = registration_data.get('name_location')

    if location_name is None:
        logger.warning(Messages.error_location_name_not_found)
        await message.answer(Messages.error_location_name_not_found)
        location_name = ''

    full_mip_report_path: str = await get_full_mip_report_name(message.chat.id, location_name=location_name)

    await create_mip_report(message,
                            # dataframe=dataframe,
                            registration_file_list=registration_file_list,
                            full_mip_report_path=full_mip_report_path,
                            violation_data=file_list
                            )

    await message.answer(f'{Messages.report_done} \n')

    # full_report_path = await get_full_report_name(message)

    # await set_report_data(message, full_mip_report_path)

    # await send_report_from_user(message, full_report_path=full_mip_report_path)

    return True
