from mimetypes import guess_type


async def get_mime_type(file_name):
    """Получить mime_type по имени файла
    :param file_name:
    :return:
    """
    mime_type = guess_type(file_name)[0]
    mime_type = mime_type if mime_type else "text/plain"

    return mime_type
