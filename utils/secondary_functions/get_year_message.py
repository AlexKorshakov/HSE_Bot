
async def get_year_message(message):
    """Обработчик сообщений с фото
    Получение полного пути файла
    """
    return str(message.date.year)