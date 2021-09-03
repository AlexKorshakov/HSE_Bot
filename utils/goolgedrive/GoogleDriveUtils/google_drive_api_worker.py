from errors.errors_decorators import retry


# @retry()
async def drive_service_files_create(drive_service, file_metadata):
    """
    :param drive_service:
    :param file_metadata:
    :return:
    """
    return drive_service.files().create(supportsTeamDrives=True, body=file_metadata).execute()


# @retry()
async def driveservice_files_create(drive_service, body, media_body, fields='id'):
    """
    :param drive_service:
    :param body:
    :param media_body:
    :param fields:
    :return:
    """
    return drive_service.files().create(body=body,
                                        media_body=media_body,
                                        fields=fields,
                                        supportsTeamDrives=True).execute()
