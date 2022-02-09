import typing

from aiogram import types
from loguru import logger

from data import board_config
from handlers.correct_entries.correct_entries_handler import delete_violation_files_from_pc, \
    delete_violation_files_from_gdrive
from keyboards.inline.build_castom_inlinekeyboard import posts_cb
from loader import dp
from messages.messages import Messages
from utils.json_worker.read_json_file import read_json_file


@dp.callback_query_handler(posts_cb.filter(action=['del_current_post']))
async def call_del_current_violation(call: types.CallbackQuery, callback_data: typing.Dict[str, str]):
    """
    :param call:
    :param callback_data:
    :return:
    """
    action: str = callback_data['action']

    if not action == 'del_current_post':
        return
    for item in board_config.violation_menu_list:
        try:
            if board_config.current_file != item:
                continue
            logger.debug(f"Выбрано: {item}")
            await call.message.edit_reply_markup()  # удаление клавиатуры
            for file in board_config.violation_file:
                if file['description'] != item:
                    continue
                violation_file = await read_json_file(file['json_full_name'])

                if not violation_file:
                    await call.message.answer(text=Messages.Error.file_not_found)
                    continue

                logger.info(
                    f"🔒 **Find  https://drive.google.com/drive/folders/{violation_file['json_folder_id']}"
                    f" in Google Drive.**")
                logger.info(
                    f"🔒 **Find  https://drive.google.com/drive/folders/{violation_file['photo_folder_id']}"
                    f" in Google Drive.**")

                # menu_level = board_config.menu_level = 1
                # menu_list = board_config.menu_list = CORRECT_COMMANDS_LIST
                # reply_markup = await add_subtract_inline_keyboard_with_action()
                # await call.message.answer(text=Messages.Admin.answer, reply_markup=reply_markup)

                await delete_violation_files_from_pc(call.message, file=file)
                await delete_violation_files_from_gdrive(call.message, file=file, violation_file=violation_file)
                board_config.current_file = None

                break
        except Exception as callback_err:
            logger.error(f"{repr(callback_err)}")
        break


@dp.callback_query_handler(posts_cb.filter(action=['correct_abort_current_post']))
async def call_del_current_violation(call: types.CallbackQuery, callback_data: typing.Dict[str, str]):
    """
    :param call:
    :param callback_data:
    :return:
    """
    action: str = callback_data['action']

    if action == 'correct_abort_current_post':
        board_config.current_file = None


@dp.callback_query_handler(posts_cb.filter(action=['correct_current_post']))
async def call_del_current_violation(call: types.CallbackQuery, callback_data: typing.Dict[str, str]):
    """
    :param call:
    :param callback_data:
    :return:
    """
    action: str = callback_data['action']

    if action == 'correct_current_post':
        await call.message.answer(text="Раздел находится в разработке")
        await call.message.answer(text=Messages.help_message)


@dp.callback_query_handler(posts_cb.filter(action=['correct_commission_composition']))
async def call_del_current_violation(call: types.CallbackQuery, callback_data: typing.Dict[str, str]):
    """
    :param call:
    :param callback_data:
    :return:
    """
    action: str = callback_data['action']

    await call.message.answer(text="Раздел находится в разработке")
    await call.message.answer(text=Messages.help_message)
