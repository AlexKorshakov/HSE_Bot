
async def get_day_message(message):
    """Обработчик сообщений с фото
    Получение номер str дня из сообщения в формате dd
    """
    return str("0" + str(message.date.day) if message.date.day < 10 else str(message.date.day))