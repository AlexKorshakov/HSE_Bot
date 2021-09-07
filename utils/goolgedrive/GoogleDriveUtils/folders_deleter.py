from loguru import logger

from utils.goolgedrive.GoogleDriveUtils.find_folder import find_file_by_name
from utils.goolgedrive.googledrive_worker import ROOT_REPORT_FOLDER_ID


async def delete_folders(drive_service, folder_names: list):
    """Удаление папок GoogleDrive
    :return:
    """
    # if folder_names is None or folder_names == []:
    #     folder_names = js.read_json_file(file="JsonData/all_folder.json")
    #
    # if drive_service is None:
    #     drive_service = drive_account_credentials(service_account_file=SERVICE_ACCOUNT_FILE,
    #                                               delegate_user=DELEGATE_USER)

    for item, f_name in enumerate(folder_names):

        if f_name["id"] == ROOT_REPORT_FOLDER_ID:
            continue

        await delete_folder(service=drive_service, folder_id=f_name["id"])
        print(f'Item {item}: delete file/folder {f_name["name"]} id {f_name["id"]}')


async def delete_folder(service, folder_id):
    """Permanently delete a file, skipping the trash.
      Args:
        service: Drive API service instance.
        folder_id: ID of the file to delete.
      """
    try:
        service.files().delete(fileId=folder_id).execute()
    except Exception as err:
        print(f'An error occurred:{err}')


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


async def del_old_data_google_drive(message, drive_service, name=None, parent=None):
    """Удаление старых данных по имени file_name  из папки folder_id
    :param message:
    :param drive_service:
    :return:
    """

    if not name:
        name = str(message.from_user.id)

    found_files = await find_file_by_name(drive_service, name=name, parent=parent)
    # pprint(found_files)

    if not found_files:
        return

    await delete_folders_for_id(drive_service, folder_id_list=found_files)


# if __name__ == '__main__':
#     """
#     """
#     message: str = "373084462"
#     drive_service = drive_account_auth_with_oauth2client(message)
#
#     # folders_name = find_all_folder(service=drive_service)
#     # folder_id_list = [folder["id"] for folder in folders_name]
#
#     folder_id_list = ['1gAh--W8NkzFpUJVfesEDjWLm_UQ4uO-U',
#                       '1qQ-KI9oPHqYpysdSEJn1escc7NhdAIZV'
#                       ]
#
#     delete_folders_for_id(drive_service=drive_service, folder_id_list=folder_id_list)

    # folders = find_all_folders(service=drive_service)
    # js.write_json_file(data=folders, name=PATH_TO_JSON + "all_folder")
