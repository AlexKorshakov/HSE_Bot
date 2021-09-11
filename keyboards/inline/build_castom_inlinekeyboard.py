from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from data import board_config
from loader import dp, bot

NUM_COL = 1
STEP_MENU = 8
move_action = CallbackData("description", "action")


async def build_inlinekeyboard(*, some_list, num_col=1, level=1) -> InlineKeyboardMarkup:
    """Создание кнопок в чате для пользователя на основе some_list.
    Колличество кнопок = колличество элементов в списке some_list
    Расположение в n_cols столбцов
    Текст на кнопках text=ss
    Возвращаемое значение, при нажатии кнопки в чате callback_data=ss
    """
    button_list = []

    if len(some_list) <= 11:
        button_list = [InlineKeyboardButton(text=ss, callback_data=ss) for ss in some_list]

        menu = await _build_menu(buttons=button_list, n_cols=num_col)

        return InlineKeyboardMarkup(resize_keyboard=True, inline_keyboard=menu)

    if 11 < len(some_list):

        end_list = len(some_list)
        start_index, stop_index = await define_indices(level, end_list)

        for batn in some_list[start_index:stop_index]:
            button_list.append(InlineKeyboardButton(text=batn, callback_data=batn))

        menu = await _build_menu(buttons=button_list, n_cols=num_col)
        reply_markup = InlineKeyboardMarkup(resize_keyboard=True, inline_keyboard=menu)

        finally_reply_markup = await add_action_button(reply_markup=reply_markup, start_index=start_index,
                                                       stop_index=stop_index, end_list=end_list)

        return finally_reply_markup


async def define_indices(level, end_list):
    """Определение начального и конечного индекса для среза на основе level
    """
    start_index = 0 if level == 1 else (STEP_MENU * level) - STEP_MENU

    if level == 1:
        start_index = 0

    stop_index = STEP_MENU if start_index == 0 else start_index + STEP_MENU

    stop_index = end_list if stop_index > end_list else start_index + STEP_MENU

    return start_index, stop_index


async def add_action_button(reply_markup, start_index, stop_index, end_list):
    """Добавление кнопок навигации в зависимости от начального (start_index),
    конечного индекса (stop_index) и конца списка list (end_list)
    :param start_index:
    :param end_list:
    :param stop_index:
    :param reply_markup:
    :return:
    """
    bt_down = InlineKeyboardButton(text="<--", callback_data=move_action.new(action="move_down"))
    bt_up = InlineKeyboardButton(text="-->", callback_data=move_action.new(action="move_up"))

    if start_index == 0:
        reply_markup.row(bt_up)
        # reply_markup.add(bt_up)
        return reply_markup

    if stop_index == end_list:
        reply_markup.row(bt_down)  # добаление кнопок в новую строку # ПРИОРИТЕТ
        # reply_markup.add(bt_down)  # добаление кнопок в конец списка
        return reply_markup

    reply_markup.row(bt_down, bt_up)
    # reply_markup.add(bt_down).add(bt_up)

    return reply_markup


async def _build_menu(buttons, n_cols: int = 1, header_buttons: list = None, footer_buttons: list = None) -> list:
    """Создание меню кнопок
    """
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu


@dp.callback_query_handler(move_action.filter(action=["move_down", "move_up"]))
async def build_inlinekeyboard_answer(call: types.CallbackQuery, callback_data: dict):
    """Обработка ответа клавиш переключения уровня меню в inlinekeyboard в сообщении
    :type callback_data: object
    :param call:
    :param callback_data:
    :return:
    """
    menu_level = board_config.menu_level
    some_list = board_config.menu_list

    chat_id = call.message.chat.id
    message_id = call.message.message_id

    if callback_data['action'] == "move_down":
        board_config.menu_level = menu_level = menu_level - 1

    if callback_data['action'] == "move_up":
        board_config.menu_level = menu_level = menu_level + 1

    reply_markup = await build_inlinekeyboard(some_list=some_list, num_col=NUM_COL, level=menu_level)

    await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=reply_markup)
