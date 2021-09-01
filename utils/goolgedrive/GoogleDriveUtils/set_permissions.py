async def get_user_permissions(drive_service, file_id: str):
    """Получение прав на редактирование файла или папки
    :param drive_service:
    :param file_id:
    :return: access
    """

    user_permission = {'type': 'user',
                       'role': 'writer',
                       'emailAddress': 'kokkaina13@gmail.com'}

    access = drive_service.permissions().create(fileId=file_id,
                                                body=user_permission,
                                                fields='id',
                                                ).execute()
    return access


async def gaining_access_drive(service, folder_id):
    """Открываем доступ на редактирование файла / папки
    :param service: any
    :param folder_id:
    :return:
    """

    body = {'type': 'user',
            'role': 'owner',
            'emailAddress': 'kokkaina13@gmail.com'}

    access = service.permissions().create(fileId=folder_id,
                                          transferOwnership=True,
                                          body=body,
                                          fields='id'
                                          ).execute()
    return access