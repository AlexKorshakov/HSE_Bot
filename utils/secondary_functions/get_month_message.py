from datetime import datetime


async def get_month_message():
    """Обработчик сообщений с фото
    Получение номер str месяца из сообщения в формате mm
    """

    current_datetime = datetime.now()
    return str("0" + str(current_datetime.month) if current_datetime.month < 10 else str(current_datetime.month))
