from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from messages.messages import Messages


async def bild_inlinekeyboar(message: types.Message, *, some_list, num_col=1) -> None:
    """Создание кнопок в чате для пользователя на основе some_list.
    Колличество кнопок = колличество элементов в списке some_list
    Расположение в n_cols столбцов
    Текст на кнопках text=ss
    Возвращаемое значение, при нажатии кнопки в чате callback_data=ss
    """

    button_list = [InlineKeyboardButton(text=ss, callback_data=ss) for ss in some_list]
    # сборка клавиатуры из кнопок `InlineKeyboardMarkup`
    menu = await _build_menu(buttons=button_list, n_cols=num_col)

    reply_markup = InlineKeyboardMarkup(resize_keyboard=True, inline_keyboard=menu)
    # отправка клавиатуры в чат
    await message.answer(text=Messages.Choose.answer, reply_markup=reply_markup)


async def _build_menu(buttons, n_cols: int = 1, header_buttons: list = None, footer_buttons: list = None) -> list:
    """Создание меню кнопок
    """
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu
