from datetime import datetime


async def get_year_message():
    """Обработчик сообщений с фото
    Получение полного пути файла
    """

    current_datetime = datetime.now()
    return str(current_datetime.year)
