from aiogram import types
from aiogram.dispatcher.filters import Command
from loguru import logger

from data import board_config
from data.category import get_names_from_json
from data.config import ADMIN_ID, DEVELOPER_ID
from keyboards.inline.build_castom_inlinekeyboard import build_inlinekeyboard
from keyboards.inline.select_category import bild_inlinekeyboar
from loader import dp

# @rate_limit(limit=20)
# @dp.message_handler(user_id=ADMIN_ID, commands=Command('admin_func'))
from messages.messages import Messages


@dp.message_handler(Command('admin_func'))
async def admin_func_handler(message: types.Message) -> None:
    """Административные функции
    :param message:
    :return:
    """
    black_list = get_names_from_json("black_list")

    if message.from_user.id != int(ADMIN_ID) or message.from_user.id != str(DEVELOPER_ID):
        logger.info(f'User @{message.from_user.username}:{message.from_user.id} looking for a admin_func')
        await message.answer(f'Меня создал https://t.me/AlexKor_MSK')

    if message.from_user.id in black_list:
        logger.info(f'User @{message.from_user.username}:{message.from_user.id} попытка доступа в админку!')
        await message.answer(f'у вас нет доступа')

    if message.from_user.id == int(ADMIN_ID) or message.from_user.id == str(DEVELOPER_ID):
        text = f"йа печенько"
        logger.info(f'User @{message.from_user.username}:{message.from_user.id} {text}')
        await message.answer(f'{text}')

        admin_menu_list = ['Показать всех пользователей', 'Редактировать профиль']
        menu_level = board_config.menu_level = 1
        menu_list = board_config.menu_list = admin_menu_list

        reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=1, level=menu_level)
        await message.answer(text=Messages.Admin.answer, reply_markup=reply_markup)

        return

    await message.answer(f'у вас нет доступа к функциям администратора')
