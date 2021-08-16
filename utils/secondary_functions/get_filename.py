from loguru import logger

from utils.secondary_functions.get_day_message import get_day_message
from utils.secondary_functions.get_month_message import get_month_message
from utils.secondary_functions.get_year_message import get_year_message


async def get_filename(message):
    """Обработчик сообщений с фото
    Получение полного пути файла
    """
    day = await get_day_message(message)
    month = await get_month_message(message)
    year = await get_year_message(message)

    str_string = len(message.photo[0].file_id)

    filename = '.'.join([day, month, year]) + \
               '___' + \
               str(message.values['from'].id) + \
               "___" + \
               str(message.photo[0].file_id[str_string-10:]) + \
               "___" + \
               str(message.message_id)

    logger.info(f"filename {filename}")
    return filename