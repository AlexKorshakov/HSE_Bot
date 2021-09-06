from pprint import pprint

from loguru import logger

from utils.goolgedrive.GoogleDriveUtils.google_drive_api_worker import drive_service_files_create

G_DRIVE_DIR_MIME_TYPE = "application/vnd.google-apps.folder"


def create_folder(service, folder_name, parent_id=None):
    """Create a folder on Drive, returns the newely created google_folders ID
    """

    root_folder = None
    folder_metadata = {'name': str(folder_name),
                       'mimeType': G_DRIVE_DIR_MIME_TYPE}

    if parent_id:
        folder_metadata['parents'] = [{'id': parent_id}]

    try:
        root_folder = service.files().create(body=folder_metadata,
                                             supportsTeamDrives=True,
                                             fields='id').execute()
        pprint(root_folder)
    except Exception as err:
        print(f'An error occurred:{err}')

    return root_folder['id']


async def create_directory(drive_service, directory_name, parent_id: str = "") -> str:
    """СОздание директории на Google Drive
    :param drive_service:
    :param directory_name: имя директории
    :param parent_id: id родительской директории
    :return: file_id
    """

    file_metadata = {
        "name": directory_name,
        "mimeType": G_DRIVE_DIR_MIME_TYPE
    }
    if parent_id:
        file_metadata["parents"] = [parent_id]

    try:
        file = await drive_service_files_create(drive_service, file_metadata)
        return file.get("id")

    except Exception as err:
        logger.error(f"get_workbook {repr(err)}")
        return ''


async def create_user_permission(drive_service, file_id, user_email):
    """Назначение прав пользователя директории
    :param drive_service:
    :param file_id: id директории
    :param user_email:
    :return:
    """

    batch = drive_service.new_batch_http_request(callback=await callback)
    for useremail in user_email:
        user_permission = {'type': 'user',
                           'role': 'writer',
                           'emailAddress': useremail['useremail']}

        batch.add(drive_service.permissions().create(fileId=file_id,
                                                     body=user_permission,
                                                     fields='id', ))
    batch.execute()


async def callback(request_id: object, response: object, exception: object) -> object:
    if exception:
        print(exception)
    else:
        print("Permission Id: %s" % response.get('id'))
