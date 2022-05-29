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


async def get_dirs_files(directory) -> list:
    """Получение списка json файлов из файловой системы
    """

    for subdir, dirs, files in os.walk(directory):
        return dirs
