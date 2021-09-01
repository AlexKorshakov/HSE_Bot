import asyncio

from loguru import logger

from utils.goolgedrive.GoogleDriveUtils.set_permissions import gaining_access_drive
from utils.goolgedrive.GoogleDriveUtils.folders_creator import create_directory
from utils.goolgedrive.GoogleDriveUtils.find_folder import find_folder_with_name


async def get_root_folder_id(drive_service, root_folder_name: str):
    """Создание основной директории в корневой директории Google Drive
    """
    root_folder_id = await find_folder_with_name(drive_service, name=str(root_folder_name))

    if not root_folder_id:
        root_folder_id = await create_directory(drive_service, directory_name=str(root_folder_name))
        await asyncio.sleep(2)
        await gaining_access_drive(drive_service, folder_id=root_folder_id)

    logger.info(f"🔒 **Find  {root_folder_id} in Google Drive.**")

    return root_folder_id


async def get_folder_id(drive_service, root_folder_name: str, parent_id):
    """Создание директориив родительской директории
    """
    folder_id = await find_folder_with_name(drive_service, name=str(root_folder_name))

    if not folder_id:
        folder_id = await create_directory(drive_service, directory_name=str(root_folder_name), parent_id=parent_id)
        await asyncio.sleep(2)
        await gaining_access_drive(drive_service, folder_id=folder_id)

    logger.info(f"🔒 **Find  {folder_id} in Google Drive.**")

    return folder_id
