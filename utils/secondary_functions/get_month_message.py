
async def get_month_message(message):
    """Обработчик сообщений с фото
    Получение полного пути файла
    """
    return str("0" + str(message.date.month) if message.date.month < 10 else str(message.date.month))