import typing

from aiogram import types
from loguru import logger

from callbacks.sequential_action.correct_headlines_data_answer import get_headlines_text
from callbacks.sequential_action.correct_registration_data_answer import get_registration_text
from callbacks.sequential_action.correct_violations_data_answer import get_violations_text
from data import board_config
from data.category import REGISTRATION_DATA_LIST, HEADLINES_DATA_LIST, VIOLATIONS_DATA_LIST
from data.config import SEPARATOR
from data.report_data import headlines_data
from handlers.correct_entries.correct_entries_handler import delete_violation_files_from_pc, \
    delete_violation_files_from_gdrive
from keyboards.inline.build_castom_inlinekeyboard import posts_cb, add_subtract_inline_keyboard_with_action, \
    build_inlinekeyboard
from loader import dp, bot
from messages.messages import Messages
from utils.generate_report.get_file_list import get_registration_json_file_list, get_json_file_list
from utils.generate_report.sheet_formatting.set_value import set_headlines_data_values
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

                try:
                    logger.info(
                        f"🔒 **Find  https://drive.google.com/drive/folders/{violation_file['json_folder_id']}"
                        f" in Google Drive.**")
                    logger.info(
                        f"🔒 **Find  https://drive.google.com/drive/folders/{violation_file['photo_folder_id']}"
                        f" in Google Drive.**")
                except KeyError as key_error:
                    logger.error(f"{repr(key_error)}")

                await delete_violation_files_from_pc(call.message, file=file)
                await delete_violation_files_from_gdrive(call.message, file=file, violation_file=violation_file)
                board_config.current_file = None

                break
        except Exception as callback_err:
            logger.error(f"{repr(callback_err)}")
        break


@dp.callback_query_handler(posts_cb.filter(action=['correct_registration_data']))
async def call_correct_registration_data(call: types.CallbackQuery, callback_data: typing.Dict[str, str]):
    """
    :param call:
    :param callback_data:
    :return:
    """
    chat_id = call.message.chat.id
    action: str = callback_data['action']
    registration_text: str = ''

    if action == 'correct_registration_data':

        registration_file_list = await get_registration_json_file_list(chat_id=chat_id)

        if not registration_file_list:
            registration_file_list = await get_registration_json_file_list(chat_id=chat_id)

        if not registration_file_list:
            logger.warning(Messages.Error.registration_file_list_not_found)
            await bot.send_message(chat_id, Messages.Error.file_list_not_found)
            return

        registration_data: dict = await read_json_file(registration_file_list)

        if not registration_data:
            logger.error(f"registration_data is empty")
            await bot.send_message(chat_id=chat_id, text=Messages.Error.file_list_not_found)
            return

        if registration_data:
            registration_text = await get_registration_text(registration_data)

        await bot.send_message(chat_id, text=registration_text)

        menu_level = board_config.menu_level = 1
        menu_list = board_config.menu_list = REGISTRATION_DATA_LIST

        reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=menu_level, level=1)

        await call.message.answer(text=Messages.Choose.entry, reply_markup=reply_markup)


@dp.callback_query_handler(posts_cb.filter(action=['correct_commission_composition']))
async def call_correct_commission_composition(call: types.CallbackQuery, callback_data: typing.Dict[str, str]):
    """
    :param call:
    :param callback_data:
    :return:
    """

    chat_id = call.message.chat.id
    action: str = callback_data['action']
    headlines_text = ''

    if action == 'correct_commission_composition':

        await set_headlines_data_values(chat_id=chat_id)

        if headlines_data:
            headlines_text = await get_headlines_text(headlines_data)

    await bot.send_message(chat_id=chat_id, text=headlines_text)

    menu_level = board_config.menu_level = 1
    menu_list = board_config.menu_list = HEADLINES_DATA_LIST

    reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=menu_level, level=1)

    await call.message.answer(text=Messages.Choose.entry, reply_markup=reply_markup)


@dp.callback_query_handler(posts_cb.filter(action=['correct_current_post']))
async def call_correct_current_post(call: types.CallbackQuery, callback_data: typing.Dict[str, str]):
    """
    :param call:
    :param callback_data:
    :return:
    """
    chat_id = call.message.chat.id
    action: str = callback_data['action']
    violations_file_path = ''

    if action == 'correct_current_post':

        violations_files_list = await get_json_file_list(chat_id)
        if not violations_files_list:
            logger.warning(Messages.Error.file_list_not_found)
            await bot.send_message(chat_id=chat_id, text=Messages.Error.file_list_not_found)
            return

        violations_id = board_config.current_file.split(' ')[0]

        for file in violations_files_list:
            if file.split('\\')[-1].split(SEPARATOR)[-1].replace('.json', '') == violations_id:
                violations_file_path = file
                break

        if not violations_file_path:
            logger.warning(f'{Messages.Error.file_not_found} violations_id: {violations_id}')
            await bot.send_message(chat_id=chat_id, text=f'{Messages.Error.file_not_found} violations_id: {violations_id}')
            return

        violations_data: dict = await read_json_file(file=violations_file_path)

        if violations_data:
            violations_text = await get_violations_text(violations_data)
            await bot.send_message(chat_id=chat_id, text=violations_text)

        menu_level = board_config.menu_level = 1
        menu_list = board_config.menu_list = VIOLATIONS_DATA_LIST

        reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=menu_level, level=1)

        await call.message.answer(text=Messages.Choose.entry, reply_markup=reply_markup)


@dp.callback_query_handler(posts_cb.filter(action=['correct_abort_current_post']))
async def call_correct_abort_current_post(call: types.CallbackQuery, callback_data: typing.Dict[str, str]):
    """
    :param call:
    :param callback_data:
    :return:
    """
    action: str = callback_data['action']

    if action == 'correct_abort_current_post':
        board_config.current_file = None
        await call.message.edit_reply_markup()  # удаление клавиатуры
        board_config.violation_menu_list: list = []
        board_config.violation_file: list = []
