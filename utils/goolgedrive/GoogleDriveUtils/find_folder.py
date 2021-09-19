import asyncio
from pathlib import Path
from typing import List, Dict

from loguru import logger

FIEDS = 'nextPageToken, files(id, name)'

async def find_folder_with_name(drive_service, *, name: str, parent=None):
    """Получение id папки по имени
    """
    q = f"name='{name}' and mimeType='application/vnd.google-apps.folder'"

    if parent:
        q = f"name='{name}' and mimeType='application/vnd.google-apps.folder' and '{parent}' in parents"

    get_folder = drive_service.files().list(
        q=q,
        spaces='drive',
        fields=FIEDS,
        pageToken=None).execute()

    await asyncio.sleep(2)

    found_folders_by_name = get_folder.get('files', [])
    for folder in found_folders_by_name:
        logger.info(f"File name: {folder.get('name')} File id: {folder.get('id')}")

    if len(found_folders_by_name) == 1:
        return found_folders_by_name[0].get('id')
    else:
        return []


async def find_folder_with_drive_id(drive_service, drive_id, recursively=True):
    """Поиск папок в папке drive_id рекурсивно если recursively=True
    :param drive_service:
    :param drive_id:
    :param recursively:
    :return:
    """
    files = drive_service.files().list(q=f"'{drive_id}' in parents",
                                       spaces='drive',
                                       pageSize=100,
                                       fields="nextPageToken, files(kind,mimeType, id, name, modifiedTime)").execute()
    returnval = []
    for file in files['files']:
        file['path'] = Path(file['name'])
        if file['mimeType'].endswith("apps.folder") and recursively:
            for subfile in await find_folder_with_drive_id(file['id'], drive_service):
                subfile['path'] = file['path'] / subfile['path']
                returnval.append(subfile)
        else:
            returnval.append(file)
    return returnval


async def find_all(service: object) -> list:
    """Получение id папки по имени
    """
    while True:
        get_folder = service.files().list().execute()

        found_folders = get_folder.get('items', [])

        for file in found_folders:
            logger.info(f"Found file: {file.get('name')} File id: {file.get('id')}")

        page_token = get_folder.get('nextPageToken', None)
        if page_token is None:
            break

    return found_folders


async def find_all_folders(drive_service) -> List[Dict[str, str]]:
    """Получение id папки по имени
    """
    page_token = None
    while True:
        get_folder = drive_service.files().list(q="mimeType='application/vnd.google-apps.folder'",
                                                spaces='drive',
                                                pageSize=400,
                                                fields='nextPageToken, files(id, name, parents)',
                                                pageToken=page_token).execute()

        found_folders = get_folder.get('files', [])

        page_token = get_folder.get('nextPageToken', None)
        if page_token is None:
            break
    return found_folders


async def find_folder_by_name(service, name, spaces='drive'):
    """Получение id папки по имени"""
    get_folder = service.files().list(q=f"name='{name}' and mimeType='application/vnd.google-apps.folder'",
                                      spaces=spaces,
                                      fields=FIEDS,
                                      pageToken=None).execute()

    found_folders_by_name = get_folder.get('files', [])

    for folder in found_folders_by_name:
        logger.info(f"File name: {folder.get('name')} File id: {folder.get('id')}")

    if len(found_folders_by_name) == 1:
        return found_folders_by_name.get('id')
    else:
        return []


async def find_file_by_name(service: object, name: str = None, is_folder: str = None, parent: str = None,
                            mime_type: str = 'application/vnd.google-apps.folder',
                            order_by="folder,name"):
    """Получение id папки по имени
    """

    q = []
    if name is not None:
        # q.append("name = '%s'" % name.replace("'", "\\'"))
        q.append(f"name contains '{name}'")

    if is_folder is not None:
        q.append("mimeType %s '%s'" % ('=' if is_folder else '!=', mime_type))

    # q.append("mimeType='application/json'")

    if parent is not None:
        q.append(f"'{parent}' in parents")

    params = {'pageToken': None, 'orderBy': order_by}

    if q:
        params['q'] = ' and '.join(q)

    get_folder = service.files().list(**params).execute()

    found_folders_by_name = get_folder.get('files', [])

    return found_folders_by_name


async def q_request_constructor(*, name: str = None, is_folder: bool = None, parent: str = None,
                                mime_type: str = 'application/vnd.google-apps.folder') -> list:
    """Конструктор q части запроса
    :param mime_type:
    :param is_folder: является ли папкой
    :param name:
    :param parent:
    :return:
    """
    q = []
    if name is not None:
        q.append(f"name contains '{name}'")

    if is_folder is not None:
        q.append(f"mimeType {'=' if is_folder else '!='} '{mime_type}'")

    if parent is not None:
        q.append(f"'{parent}' in parents")

    return q


async def params_constructor(q: list = None, spaces='drive', page_size: int = 100, order_by=None, p_fields: str = None,
                             files: str = None):
    """Конструктор параметров запроса
    :param files:
    :param p_fields:
    :param order_by:
    :param page_size:
    :param spaces:
    :param q:
    :return:
    """

    params = {'pageToken': None, 'pageSize': page_size}

    if q:
        params['q'] = ' and '.join(q)

    if order_by:
        params['orderBy'] = order_by

    if spaces:
        params['spaces'] = spaces

    if p_fields is None:
        params['fields'] = FIEDS

    if files:
        request_text = f'nextPageToken, files({files})'
        params['fields'] = request_text

    return params


async def find_files_or_folders_list(drive_service, *, params: dict) -> list:
    """Поик на drive_service по заданным параметрам
    :return:
    """
    try:

        get_folder = drive_service.files().list(**params).execute()
        found_folders_by_name = get_folder.get('files', [])
        return found_folders_by_name

    except Exception as err:
        logger.error(f"{repr(err)}")
        return []
