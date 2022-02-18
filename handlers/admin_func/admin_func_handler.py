import os

from aiogram import types
from aiogram.dispatcher.filters import Command
from loguru import logger

from data import board_config
from data.category import get_names_from_json, ADMIN_MENU_LIST
from data.config import ADMIN_ID, DEVELOPER_ID, BOT_DATA_PATH
from keyboards.inline.build_castom_inlinekeyboard import build_inlinekeyboard

from loader import dp
from messages.messages import Messages
from states import DataUserState
from utils.custom_filters import is_private
from utils.json_worker.read_json_file import read_json_file
from utils.secondary_functions.get_json_files import get_dirs_files


@dp.message_handler(Command('admin_func'))
async def admin_func_handler(message: types.Message) -> None:
    """Административные функции
    :param message:
    :return:
    """
    black_list = get_names_from_json("black_list")
    chat_id = message.chat.id

    if chat_id != int(ADMIN_ID) or chat_id != int(DEVELOPER_ID):
        logger.info(f'User @{message.from_user.username}:{message.from_user.id} looking for a admin_func')
        await message.answer(f'Меня создал https://t.me/AlexKor_MSK')

    if chat_id in black_list:
        logger.info(f'User @{message.from_user.username}:{chat_id} попытка доступа в админку!')
        await message.answer(f'у вас нет доступа')

    if chat_id == int(ADMIN_ID) or message.from_user.id == int(DEVELOPER_ID):
        # text = f"йа печенько"
        # logger.info(f'User @{message.from_user.username}:{message.from_user.id} {text}')
        # await message.answer(f'{text}')

        menu_level = board_config.menu_level = 1
        menu_list = board_config.menu_list = ADMIN_MENU_LIST

        reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=1, level=menu_level)
        await message.answer(text=Messages.Admin.answer, reply_markup=reply_markup)

        return

    await message.answer(f'у вас нет доступа к функциям администратора')


@dp.callback_query_handler(is_private, lambda call: call.data in [item for item in ADMIN_MENU_LIST])
async def correct_registration_data_work_shift_answer(call: types.CallbackQuery):
    """Обработка ответов содержащихся в WORK_SHIFT
    """
    # chat_id = call.message.chat.id
    files: list = await get_dirs_files(BOT_DATA_PATH)

    if call.data == 'Показать всех пользователей':

        users_data: list = []
        for file in files:

            file_path = f'{BOT_DATA_PATH}\\{file}\\{file}.json'
            if not os.path.isfile(file_path):
                continue
            file_dict: dict = await read_json_file(file_path)

            try:
                name = file_dict['name'].lstrip(' ').rstrip(' ')
            except KeyError:
                name = 'Нет описания'

            user_id: str = f"{file_dict['user_id']} {name.split(' ')[0]}"

            users_data.append(user_id)

        menu_level = board_config.menu_level = 1
        menu_list = board_config.menu_list = users_data

        reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=1, level=menu_level)
        await call.message.answer(text=Messages.Admin.answer, reply_markup=reply_markup)

        await DataUserState.user_data.set()
