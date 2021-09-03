import asyncio

from loguru import logger

from utils.goolgedrive.GoogleDriveUtils.set_permissions import gaining_access_drive
from utils.goolgedrive.GoogleDriveUtils.folders_creator import create_directory
from utils.goolgedrive.GoogleDriveUtils.find_folder import find_folder_with_name


async def get_report_folder_id(drive_service, report_folder_name: str, parent_id=None):
    """Создание основной директории хранения report в директории пользователя на Google Drive
    """
    report_folder_id = await find_folder_with_name(drive_service, name=str(report_folder_name))

    if not report_folder_id:
        report_folder_id = await create_directory(drive_service,
                                                  directory_name=str(report_folder_name),
                                                  parent_id=parent_id)
        await asyncio.sleep(2)
        await gaining_access_drive(drive_service, folder_id=report_folder_id)
        return report_folder_id

    logger.info(f"🔒 **Find  {report_folder_id} in Google Drive.**")

    return report_folder_id


async def get_photo_folder_id(drive_service, photo_folder_name: str, parent_id=None):
    """Создание основной директории хранения photo в директории пользователя на Google Drive
    """
    photo_folder_id = await find_folder_with_name(drive_service, name=str(photo_folder_name))

    if not photo_folder_id:
        photo_folder_id = await create_directory(drive_service,
                                                 directory_name=str(photo_folder_name),
                                                 parent_id=parent_id)
        await asyncio.sleep(2)
        await gaining_access_drive(drive_service, folder_id=photo_folder_id)
        return photo_folder_id

    logger.info(f"🔒 **Find  {photo_folder_id} in Google Drive.**")

    return photo_folder_id


async def get_json_folder_id(drive_service, json_folder_name: str, parent_id=None):
    """Создание основной директории хранения json в директории пользователя на Google Drive
    """
    json_folder_id = await find_folder_with_name(drive_service, name=str(json_folder_name))

    if not json_folder_id:
        json_folder_id = await create_directory(drive_service,
                                                directory_name=str(json_folder_name),
                                                parent_id=parent_id)
        await asyncio.sleep(2)
        await gaining_access_drive(drive_service, folder_id=json_folder_id)
        return json_folder_id

    logger.info(f"🔒 **Find  {json_folder_id} in Google Drive.**")

    return json_folder_id


async def get_root_folder_id(drive_service, root_folder_name: str):
    """Создание основной директории в корневой директории Google Drive
    """
    root_folder_id = await find_folder_with_name(drive_service, name=str(root_folder_name))

    if not root_folder_id:
        root_folder_id = await create_directory(drive_service,
                                                directory_name=str(root_folder_name))
        await asyncio.sleep(2)
        await gaining_access_drive(drive_service, folder_id=root_folder_id)
        return root_folder_id

    logger.info(f"🔒 **Find  {root_folder_id} in Google Drive.**")

    return root_folder_id


async def get_user_folder_id(drive_service, root_folder_name: str, parent_id):
    """Создание директориив родительской директории
    """
    user_folder_id = await find_folder_with_name(drive_service, name=str(root_folder_name))

    if not user_folder_id:
        user_folder_id = await create_directory(drive_service,
                                                directory_name=str(root_folder_name),
                                                parent_id=parent_id)
        await asyncio.sleep(2)
        await gaining_access_drive(drive_service, folder_id=user_folder_id)
        return user_folder_id

    logger.info(f"🔒 **Find  {user_folder_id} in Google Drive.**")

    return user_folder_id
