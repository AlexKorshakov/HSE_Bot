import asyncio
from pathlib import Path
from typing import List, Dict

from loguru import logger


async def find_folder_with_name(drive_service, name: str):
    """Получение id папки по имени
    """
    get_folder = drive_service.files().list(q=f"name='{name}' and mimeType='application/vnd.google-apps.folder'",
                                            spaces='drive',
                                            fields='nextPageToken, files(id, name)',
                                            pageToken=None).execute()
    await asyncio.sleep(2)
    found_folders_by_name = get_folder.get('files', [])
    for folder in found_folders_by_name:
        logger.info(f"File name: {folder.get('name')} File id: {folder.get('id')}")

    if len(found_folders_by_name) == 1:
        return found_folders_by_name[0].get('id')
    else:
        return found_folders_by_name


async def find_folder_with_drive_id(drive_service, drive_id, recursively=True):
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
    """Получение id папки по имени"""

    while True:
        get_folder = service.files().list().execute()

        found_folders = get_folder.get('items', [])

        for file in found_folders:
            print(f"Found file: {file.get('name')} File id: {file.get('id')}")

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
                                      fields='nextPageToken, files(id, name)',
                                      pageToken=None).execute()

    found_folders_by_name = get_folder.get('files', [])
    for folder in found_folders_by_name:
        print(f"File name: {folder.get('name')} File id: {folder.get('id')}")

    if len(found_folders_by_name) == 1:
        return found_folders_by_name.get('id')
    else:
        return found_folders_by_name


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

    q.append("mimeType='application/json'")

    if parent is not None:
        q.append(f"'{parent}' in parents")

    params = {'pageToken': None, 'orderBy': order_by}
    if q:
        params['q'] = ' and '.join(q)

    get_folder = service.files().list(**params).execute()

    found_folders_by_name = get_folder.get('files', [])

    return found_folders_by_name