from data.config import BOT_DATA_PATH, JSON_DATA_PATH, PHOTO_DATA_PATH


async def get_filepath(name):
    """Обработчик сообщений с фото
    Получение полного пути файла
    """
    name = name + ".jpg"
    filepath = BOT_DATA_PATH + name

    return filepath

async def get_json_filepath(name):
    """Обработчик сообщений с фото
    Получение полного пути файла
    """
    return JSON_DATA_PATH + name

async def get_photo_filepath(name):
    """Обработчик сообщений с фото
    Получение полного пути файла
    """
    name = name + ".jpg"
    filepath = PHOTO_DATA_PATH + name

    return filepath