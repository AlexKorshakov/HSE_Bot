from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters import Text

# from callbacks.callback_action import move_action
# from loader import dp, bot


async def bild_inlinekeyboar(message: types.Message, *, some_list, num_col=1) -> None:
    """Создание кнопок в чате для пользователя на основе some_list.
    Колличество кнопок = колличество элементов в списке some_list
    Расположение в n_cols столбцов
    Текст на кнопках text=ss
    Возвращаемое значение, при нажатии кнопки в чате callback_data=ss
    """

    # if len(some_list) <= 10:
    button_list = [InlineKeyboardButton(text=ss, callback_data=ss) for ss in some_list]
    # сборка клавиатуры из кнопок `InlineKeyboardMarkup`
    menu = await _build_menu(buttons=button_list, n_cols=num_col)

    reply_markup = InlineKeyboardMarkup(resize_keyboard=True, inline_keyboard=menu)
    # отправка клавиатуры в чат
    await message.answer(text="Выберите ответ", reply_markup=reply_markup)

    # else:
    #
    #     iter: int = len(some_list)
    #     await message.answer(text="Выберите ответ",
    #                          parse_mode="markdown",
    #                          disable_notification=True,
    #                          reply_markup=InlineKeyboardMarkup(await map(pos=iter))
    #                          )


# callback_filter = Filters.create(lambda _, query: query.data.startswith('help+'))


# @dp.callback_query_handler(move_action.filter(action=["move_up"]))
# async def help_answer(call: types.CallbackQuery, callback_data: dict):
#     chat_id = call.message.from_user.id
#     message_id = call.message.message_id
#     msg = int(callback_data.data.split('+')[1])
#
#     await bot.edit_message_text(chat_id=chat_id, message_id=message_id,
#                                 text=tr.HELP_MSG[msg], reply_markup=InlineKeyboardMarkup(map(msg)))
#
#
# async def map(pos: int):
#     if (pos == 1):
#         button = [
#             [InlineKeyboardButton(text='-->', callback_data=f"move_up")]
#         ]
#     elif (pos == len(tr.HELP_MSG) - 1):
#
#         button = [
#             [InlineKeyboardButton(text='Support Chat', callback_data="https://www.github.com/cdfxscrq")],
#             [InlineKeyboardButton(text='Feature Request', url="https://t.me/Akshayan1")],
#             [InlineKeyboardButton(text='<--', callback_data=f"help+{pos - 1}")]
#         ]
#     else:
#         button = [
#             [
#                 InlineKeyboardButton(text='<--', callback_data=f"move_down"),
#                 InlineKeyboardButton(text='-->', callback_data=f"move_up")
#             ],
#         ]
#     return button


async def _build_menu(buttons, n_cols: int = 1, header_buttons: list = None, footer_buttons: list = None) -> list:
    """Создание меню кнопок
    """
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu
