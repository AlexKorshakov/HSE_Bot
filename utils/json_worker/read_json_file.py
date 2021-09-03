import json


async def read_json_file(file):
    """Чтение данных из json
    """
    with open(file, 'r', encoding='utf8') as data_file:
        data_loaded = json.load(data_file)
    return data_loaded


async def read_json_files(files, data):
    """Чтение данных из json
    """

    for item in files:
        data.append(await read_json_file(item))

    return data

