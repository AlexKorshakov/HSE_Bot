from loguru import logger

from utils.goolgedrive.GoogleDriveUtils.find_folder import find_file_by_name
from utils.goolgedrive.googledrive_worker import ROOT_REPORT_FOLDER_ID


async def delete_folders(drive_service, folder_names: list):
    """Удаление папок GoogleDrive
    :return:
    """

    for item, f_name in enumerate(folder_names):

        if f_name["id"] == ROOT_REPORT_FOLDER_ID:
            continue

        await delete_folder(service=drive_service, folder_id=f_name["id"])
        logger.info(f'Item {item}: delete file/folder {f_name["name"]} id {f_name["id"]}')


async def delete_folder(service, folder_id) -> bool:
    """Permanently delete a file, skipping the trash.
      Args:
        service: Drive API service instance.
        folder_id: ID of the file to delete.
      """
    try:
        service.files().delete(fileId=folder_id).execute()
        return True
    except Exception as err:
        logger.error(f'An error occurred:{err}')
        return False


async def delete_folders_for_id(drive_service, folder_id_list: list):
    """Удаление файлов или папки по id
    :param drive_service:
    :param folder_id_list:
    :return:
    """
    for item, f_id in enumerate(folder_id_list, start=1):

        if f_id["id"] == ROOT_REPORT_FOLDER_ID:
            continue

        await delete_folder(service=drive_service, folder_id=f_id["id"])
        logger.info(f'Item {item}: delete file/folder {f_id["name"]} id {f_id["id"]}')


async def del_by_name_old_data_google_drive(*, chat_id, drive_service, name=None, parent=None):
    """Удаление старых данных по имени file_name  из папки folder_id
    :param parent:
    :param name:
    :param chat_id:
    :param drive_service:
    :return:
    """

    if not name:
        name = str(chat_id)

    found_files = await find_file_by_name(drive_service, name=name, parent=parent)

    if not found_files:
        return

    await delete_folders_for_id(drive_service, folder_id_list=found_files)
