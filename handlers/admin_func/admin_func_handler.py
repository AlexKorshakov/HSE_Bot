import os
import time

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger

from data import board_config
from data.category import ADMIN_MENU_LIST
from data.config import ADMIN_ID, DEVELOPER_ID, BOT_DATA_PATH
from keyboards.inline.build_castom_inlinekeyboard import build_inlinekeyboard
from loader import dp
from messages.messages import Messages
from utils.custom_filters import is_private
from utils.json_worker.read_json_file import read_json_file
from utils.misc import rate_limit
from utils.notify_admins import admin_notify
from utils.secondary_functions.get_json_files import get_dirs_files
from utils.secondary_functions.check_user_registration import check_user_access


@rate_limit(limit=10)
@dp.message_handler(Command('admin_func'))
async def admin_func_handler(message: types.Message) -> None:
    """Административные функции
    :param message:
    :return:
    """

    chat_id = message.chat.id

    if not await check_user_access(chat_id=chat_id):
        return

    if chat_id != int(ADMIN_ID) or chat_id != int(DEVELOPER_ID):
        await admin_notify(
            user_id=chat_id,
            notify_text=f'User @{message.from_user.username}:{chat_id} попытка доступа в админку!'
        )

        await message.answer(
            text=f'У Вас нет прав доступа к административным функциям!\n'
                 f'По всем вопросам обращайтесь к администратору\n'
                 f'https://t.me/AlexKor_MSK',
            disable_web_page_preview=True)

        return

    if chat_id == int(ADMIN_ID) or message.from_user.id == int(DEVELOPER_ID):

        menu_level = board_config.menu_level = 1
        menu_list = board_config.menu_list = ADMIN_MENU_LIST

        reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=1, level=menu_level)
        await message.answer(text=Messages.Admin.answer, reply_markup=reply_markup)

        return

    await message.answer(f'у вас нет доступа к функциям администратора')


@dp.callback_query_handler(is_private, lambda call: call.data in [item for item in ADMIN_MENU_LIST])
async def admin_function_answer(call: types.CallbackQuery):
    """Обработка ответов содержащихся в ADMIN_MENU_LIST
    """

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

    if call.data == 'Оповещение':

        text: str = 'Приветствую! \n' \
                    'Бот MIP_HSE_BOT обновился!\n' \
                    '\n' \
                    'Команда: Изменение данных или /correct_entries\n' \
                    'добавлено: \n' \
                    'коррекция данных регистрации \n' \
                    'возможно исправить \n' \
                    '    ФИО\n' \
                    '    Должность\n' \
                    '    Площалку\n' \
                    '    Смена\n' \
                    '    Телефон\n' \
                    '\n' \
                    'коррекция данных зарегистрированных нарушений\n' \
                    'возможно исправить \n' \
                    '    Описание нарушения\n' \
                    '    Комментарий к нарушению\n' \
                    '    Основное направление\n' \
                    '    Количество дней на устранение\n' \
                    '    Степень опасности ситуации\n' \
                    '    Требуется ли оформление акта?\n' \
                    '    Подрядная организация\n' \
                    '    Категория нарушения\n' \
                    '    Уровень происшествия\n' \
                    '\n' \
                    'коррекция данных заголовков отчета (Состав комиссии)\n' \
                    'возможно исправить \n' \
                    '    Руководитель строительства\n' \
                    '    Инженер СК\n' \
                    '    Подрядчик\n' \
                    '    Субподрядчик\n' \
                    '    Вид обхода\n' \
                    '    Представитель подрядчика\n' \
                    '    Представитель субподрядчика\n' \
                    '\n' \
                    'где возможно - добавлен выбор данных из списка\n' \
                    'в остальных случаях - ручной ввод\n' \
                    '\n' \
                    'команда отмены или /cansel прекращает все действия во всех процессах бота\n' \
                    'работает из любого места или меню\n' \
                    '\n' \
                    'исправлены ошибки повышена стабильность работы\n' \
                    '\n' \
                    'По всем вопросам - к разработчику\n' \
                    f'{Messages.help_message}'

        for user_id in files:

            if user_id == ADMIN_ID: continue

            reply_markup = InlineKeyboardMarkup()
            reply_markup.add(InlineKeyboardButton(text='написать разработчику', url=f"tg://user?id={ADMIN_ID}"))

            try:

                await dp.bot.send_message(chat_id=user_id, text=text, reply_markup=reply_markup)

            except Exception as err:
                logger.error(f'bot.send_message error {repr(err)}')
                dp.bot.send_message(chat_id=ADMIN_ID,
                                    text=f'bot.send_message error user_id')
                continue

            await admin_notify(
                user_id=user_id,
                notify_text=f'Оповещение отправлено {user_id}'
            )
            time.sleep(1)
