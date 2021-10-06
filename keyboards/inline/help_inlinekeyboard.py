from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def help_inline_button():
    """Формирование кнопок и клавиатуры Справки по команде / help
    :return:
    """
    btn_1 = InlineKeyboardButton(
        '1.Регистрация пользователя',
        url='https://www.youtube.com/watch?v='
            'C50_wKIN2DQ&list=PLbHi3cvK0ys4om-vad17AmtIt-y0sHOxI&index=1&ab_channel=АлексейКоршаков'
    )
    btn_2 = InlineKeyboardButton(
        '2. Регистрация несоответствий',
        url='https://www.youtube.com/watch?v='
            'cdPuUoV_P5g&list=PLbHi3cvK0ys4om-vad17AmtIt-y0sHOxI&index=2&ab_channel=АлексейКоршаков'
    )

    btn_3 = InlineKeyboardButton(
        '3. Удаление зарегестрированных несоответствий',
        url='https://www.youtube.com/watch?v='
            'wQyLRrPqNfI&list=PLbHi3cvK0ys4om-vad17AmtIt-y0sHOxI&index=3&ab_channel=АлексейКоршаков'
    )
    btn_4 = InlineKeyboardButton(
        '4. Формирование отчетов',
        url='https://www.youtube.com/watch?v='
            'cdPuUoV_P5g&list=PLbHi3cvK0ys4om-vad17AmtIt-y0sHOxI&index=4&ab_channel=АлексейКоршаков'
    )
    btn_5 = InlineKeyboardButton(
        '5. Админка',
        url='https://www.youtube.com/watch?v='
            'cdPuUoV_P5g&list=PLbHi3cvK0ys4om-vad17AmtIt-y0sHOxI&index=5&ab_channel=АлексейКоршаков'
    )
    btn_6 = InlineKeyboardButton(
        '6. Отправка отчета по email',
        url='https://www.youtube.com/watch?v='
            'cdPuUoV_P5g&list=PLbHi3cvK0ys4om-vad17AmtIt-y0sHOxI&index=6&ab_channel=АлексейКоршаков'
    )

    inline_kb_full = InlineKeyboardMarkup(row_width=1)
    inline_kb_full.add(btn_1)
    inline_kb_full.add(btn_2)
    inline_kb_full.add(btn_3)
    inline_kb_full.add(btn_4)
    # inline_kb_full.add(btn_5)
    # inline_kb_full.add(btn_6)

    return inline_kb_full
