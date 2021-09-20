import os


async def get_files(main_path, endswith=".json") -> list:
    """Получение списка json файлов из файловой системы
    """
    json_files = []
    for subdir, dirs, files in os.walk(main_path):
        for file in files:
            filepath = subdir + os.sep + file
            if filepath.endswith(endswith):
                json_files.append(filepath)
    return json_files
