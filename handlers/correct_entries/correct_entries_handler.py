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
        logger.warning(Messages.error_file_list_not_found)
        await bot.send_message(message.from_user.id, Messages.error_file_list_not_found)

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
    await message.answer(text="Выберите запись по id", reply_markup=reply_markup)


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

                logger.info(
                    f"🔒 **Find  https://drive.google.com/drive/folders/{violation_file['json_folder_id']} in Google Drive.**")
                logger.info(
                    f"🔒 **Find  https://drive.google.com/drive/folders/{violation_file['photo_folder_id']} in Google Drive.**")

                await del_file(call.message, path=file['json_full_name'])
                await del_file(call.message, path=file['photo_full_name'])

                await del_file_from_gdrive(call.message, file, violation_file)

                break

                # await call.message.answer(text=Messages.error_file_not_found)
            break

        except Exception as callback_err:
            logger.error(f"{repr(callback_err)}")


async def del_file(message, path):
    if os.path.isfile(path):
        await message.answer(text=Messages.violation_removed)
        os.remove(path)


async def del_file_from_gdrive(message, file, violation_file):
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

    mime_type: str = str(guess_type(violation_file['json_full_name'])[0])
    q = await q_request_constructor(name=name,
                                    parent=violation_file['json_folder_id'],
                                    mime_type=mime_type
                                    )
    params = await params_constructor(q=q, spaces="drive")
    v_files = await find_files_or_folders_list(drive_service, params=params)
    for v in v_files:
        if v.get("id"):
            await delete_folder(service=drive_service, folder_id=v["id"])
    pprint(v_files)

    mime_type: str = str(guess_type(violation_file['photo_full_name'])[0])
    q = await q_request_constructor(name=name,
                                    parent=violation_file['photo_folder_id'],
                                    mime_type=mime_type
                                    )
    params = await params_constructor(q=q, spaces="drive")
    v_files = await find_files_or_folders_list(drive_service, params=params)
    for v in v_files:
        if v.get("id"):
            await delete_folder(service=drive_service, folder_id=v["id"])
    pprint(v_files)
