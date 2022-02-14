from datetime import datetime


async def get_day_message():
    """Обработчик сообщений с фото
    Получение номер str дня из сообщения в формате dd
    """

    current_datetime = datetime.now()

    return str("0" + str(current_datetime.day) if current_datetime.day < 10 else str(current_datetime.day))
