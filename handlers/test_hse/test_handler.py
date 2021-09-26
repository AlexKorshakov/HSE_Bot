import os
from pprint import pprint

from aiogram import types
from aiogram.dispatcher.filters import Command
from loguru import logger

from mimetypes import guess_type

from data import board_config
from data.config import BOT_DATA_PATH, SEPARATOR
from keyboards.inline.build_castom_inlinekeyboard import build_inlinekeyboard
from loader import bot, dp
from messages.messages import Messages
# from utils.generate_report.get_file_list import get_json_file_list
# from utils.secondary_functions.get_filepath import get_json_full_filepath
from utils.goolgedrive.GoogleDriveUtils.GoogleDriveWorker import drive_account_credentials
from utils.goolgedrive.GoogleDriveUtils.find_folder import q_request_constructor, params_constructor, \
    find_files_or_folders_list, find_file_by_name, find_folder_with_drive_id
from utils.goolgedrive.GoogleDriveUtils.folders_deleter import delete_folders_for_id, delete_folder
from utils.json_worker.read_json_file import read_json_file
from utils.secondary_functions.get_json_files import get_files


@dp.message_handler(Command('test'))
async def test_2(message: types.Message):
    pass
#     violation_description: list = []
#     violation_file: list = []
#
#     user_id = 373084462
#     file_list = await get_json_file_list(user_id)
#     if not file_list:
#         logger.warning(Messages.error_file_list_not_found)
#         await bot.send_message(user_id, Messages.error_file_list_not_found)
#
#     for file_path in file_list:
#
#         file = await read_json_file(file_path)
#
#         if file.get("violation_id"):
#             violation_id = file.get("violation_id")
#         else:
#             violation_id = file.get("file_id").split(SEPARATOR)[-1]
#
#         violation_description.append(
#             f"{violation_id} {file.get('description')[:25]}..."
#         )
#         violation_file.append(
#             {"violation_id": f"{violation_id}",
#              "description": f"{violation_id} {file.get('description')[:25]}...",
#              "file_path": f"{file_path}",
#              }
#         )
#
#     menu_level = board_config.menu_level = 1
#     board_config.violation_file = violation_file
#     menu_list = board_config.violation_menu_list = violation_description
#
#     reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=1, level=menu_level)
#     await message.answer(text="Выберите запись по id", reply_markup=reply_markup)


# async def get_json_file_list(message) -> list:
#     """Получение списка файлов из директории
#     """
#     # json_data_path = await get_json_full_filepath(str(373084462))
#
#     json_data_path = f"{BOT_DATA_PATH}\\{message}\\data_file\\23.09.2021\\json"
#
#     files = await get_files(json_data_path)
#     global_data = []
#
#     for file in files:
#         # current_date = file.split(SEPARATOR)[1]
#         #
#         # if str(current_date.split(".")[0]) == await get_day_message(message) and \
#         #         str(current_date.split(".")[1]) == await get_month_message(message) and \
#         #         str(file.split(SEPARATOR)[2]) == str(message.from_user.id):
#         #     global_data.append(file)
#         global_data.append(file)
#     return global_data


# @dp.callback_query_handler(lambda call: call.data in board_config.violation_menu_list)
# async def violation_id_answer(call: types.CallbackQuery):
#     """Обработка ответов содержащихся в CATEGORY_LIST
#     """
#     for i in board_config.violation_menu_list:
#         try:
#             if call.data == i:
#                 logger.debug(f"Выбрано: {i}")
#
#                 for file in board_config.violation_file:
#                     if file['description'] != i:
#                         continue
#                     if os.path.isfile(file['file_path']):
#                         logger.debug(f"Выбрано: {i}")
#                         await call.message.answer(text=Messages.violation_removed)
#                         # os.remove(file['file_path'])
#
#                         violation_file = await read_json_file(file['file_path'])
#
#                         logger.info(
#                             f"🔒 **Find  https://drive.google.com/drive/folders/{violation_file['json_folder_id']} in Google Drive.**")
#                         logger.info(
#                             f"🔒 **Find  https://drive.google.com/drive/folders/{violation_file['photo_folder_id']} in Google Drive.**")
#
#                         drive_service = await drive_account_credentials(chat_id=call.message.chat.id)
#
#                         if file.get("violation_id"):
#                             name: str = file.get("violation_id")
#                         else:
#                             name: str = file.get("file_id")
#
#                         mime_type: str = str(guess_type(violation_file['json_full_name'])[0])
#                         q = await q_request_constructor(name=name,
#                                                         parent=violation_file['json_folder_id'],
#                                                         mime_type=mime_type
#                                                         )
#                         params = await params_constructor(q=q, spaces="drive")
#                         v_files = await find_files_or_folders_list(drive_service, params=params)
#                         for v in v_files:
#                             if v.get("id"):
#                                 await delete_folder(service=drive_service, folder_id=v["id"])
#
#                         pprint(v_files)
#
#                         mime_type: str = str(guess_type(violation_file['photo_full_name'])[0])
#                         q = await q_request_constructor(name=name,
#                                                         parent=violation_file['photo_folder_id'],
#                                                         mime_type=mime_type
#                                                         )
#                         params = await params_constructor(q=q, spaces="drive")
#                         v_files = await find_files_or_folders_list(drive_service, params=params)
#                         pprint(v_files)
#
#                         break
#                     else:
#                         await call.message.answer(text=Messages.error_file_not_found)
#                 break
#
#         except Exception as callback_err:
#             logger.error(f"{repr(callback_err)}")
