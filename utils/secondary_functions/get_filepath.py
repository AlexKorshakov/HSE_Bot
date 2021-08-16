from data.config import BOT_DATA_PATH


async def get_filepath(name):
    """Обработчик сообщений с фото
    Получение полного пути файла
    """
    name = name + ".jpg"
    filepath = BOT_DATA_PATH + name

    return filepath