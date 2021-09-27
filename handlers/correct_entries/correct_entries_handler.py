import os
from mimetypes import guess_type
from pprint import pprint

from aiogram import types
from aiogram.dispatcher.filters import Command
from loguru import logger

from data import board_config
from data.config import SEPARATOR
from keyboards.inline.build_castom_inlinekeyboard import build_inlinekeyboard
from loader import dp, bot
from messages.messages import Messages
from utils.generate_report.get_file_list import get_json_file_list
from utils.goolgedrive.GoogleDriveUtils.GoogleDriveWorker import drive_account_credentials
from utils.goolgedrive.GoogleDriveUtils.find_folder import q_request_constructor, params_constructor, \
    find_files_or_folders_list
from utils.goolgedrive.GoogleDriveUtils.folders_deleter import delete_folder
from utils.json_worker.read_json_file import read_json_file


@dp.message_handler(Command('correct_entries'))
async def correct_entries(message: types.Message):
    """Корректирование уже введённых значений на локальном pc и на google drive
    :return:
    """
    violation_description: list = []
    violation_file: list = []

    file_list = await get_json_file_list(message)

    if not file_list:
        logger.warning(Messages.Error.file_list_not_found)
        await bot.send_message(message.from_user.id, Messages.Error.file_list_not_found)

    for file_path in file_list:

        file = await read_json_file(file_path)

        if file.get("violation_id"):
            violation_id = file.get("violation_id")
        else:
            violation_id = file.get("file_id").split(SEPARATOR)[-1]

        violation_description.append(
            f"{violation_id} {file.get('description')[:25]}..."
        )
        violation_file.append(
            {"violation_id": f"{violation_id}",
             "description": f"{violation_id} {file.get('description')[:25]}...",
             "json_full_name": f"{file.get('json_full_name')}",
             "photo_full_name": f"{file.get('photo_full_name')}"
             }
        )

    menu_level = board_config.menu_level = 1
    board_config.violation_file = violation_file
    menu_list = board_config.violation_menu_list = violation_description

    reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=1, level=menu_level)
    await message.answer(text=Messages.Choose.entry, reply_markup=reply_markup)


@dp.callback_query_handler(lambda call: call.data in board_config.violation_menu_list)
async def violation_id_answer(call: types.CallbackQuery):
    """Обработка ответов содержащихся в CATEGORY_LIST
    """
    for item in board_config.violation_menu_list:
        try:
            if call.data != item:
                continue
            logger.debug(f"Выбрано: {item}")

            for file in board_config.violation_file:
                if file['description'] != item:
                    continue
                violation_file = await read_json_file(file['json_full_name'])

                if not violation_file:
                    await call.message.answer(text=Messages.Error.file_not_found)
                    continue

                logger.info(
                    f"🔒 **Find  https://drive.google.com/drive/folders/{violation_file['json_folder_id']} in Google Drive.**")
                logger.info(
                    f"🔒 **Find  https://drive.google.com/drive/folders/{violation_file['photo_folder_id']} in Google Drive.**")

                await delete_violation_files_from_pc(call.message, file=file)
                await delete_violation_files_from_gdrive(call.message, file=file, violation_file=violation_file)
                break

            break

        except Exception as callback_err:
            logger.error(f"{repr(callback_err)}")


async def delete_violation_files_from_pc(message: types.Message, file):
    """Удаление файлов из памяти pc
    :param message:
    :param file:
    :return:
    """
    if not await del_file(path=file['json_full_name']):
        await bot.message.answer(text=Messages.Error.file_not_found)
    await message.answer(text=Messages.Removed.violation_data_pc)

    if not await del_file(path=file['photo_full_name']):
        await message.answer(text=Messages.Error.file_not_found)
    await message.answer(text=Messages.Removed.violation_photo_pc)


async def del_file(path) -> bool:
    """Удаление файла из памяти pc
    :param path:
    :return:
    """
    if os.path.isfile(path):
        os.remove(path)
        return True
    return False


async def delete_violation_files_from_gdrive(message, file, violation_file):
    """Удаление файлов из google drive
    :param violation_file:
    :param file:
    :param message:
    :return:
    """

    drive_service = await drive_account_credentials(chat_id=message.chat.id)

    if file.get("violation_id"):
        name: str = file.get("violation_id")
    else:
        name: str = file.get("file_id")

    violation_data_file = violation_file['json_full_name']
    violation_data_parent_id = violation_file['json_folder_id']

    if not await del_file_from_gdrive(drive_service,
                                      name=name,
                                      violation_file=violation_data_file,
                                      parent_id=violation_data_parent_id):
        await message.answer(text=Messages.Error.file_not_found)
    await message.answer(text=Messages.Removed.violation_data_gdrive)

    violation_photo_file = violation_file['photo_full_name']
    violation_photo_parent_id = violation_file['photo_folder_id']

    if not await del_file_from_gdrive(drive_service,
                                      name=name,
                                      violation_file=violation_photo_file,
                                      parent_id=violation_photo_parent_id):
        await message.answer(text=Messages.Error.file_not_found)
    await message.answer(text=Messages.Removed.violation_photo_gdrive)


async def del_file_from_gdrive(drive_service, *, name, violation_file, parent_id) -> bool:
    """Удаление файлов из google drive
    :param parent_id:
    :param violation_file:
    :param name:
    :param drive_service:
    :return:
    """

    mime_type: str = str(guess_type(violation_file)[0])
    q = await q_request_constructor(name=name,
                                    parent=parent_id,
                                    mime_type=mime_type
                                    )
    params = await params_constructor(q=q, spaces="drive")
    v_files = await find_files_or_folders_list(drive_service, params=params)
    pprint(f"find_files {v_files}")

    for v in v_files:
        if v.get("id"):
            return True if await delete_folder(service=drive_service, folder_id=v["id"]) else False
    return False
