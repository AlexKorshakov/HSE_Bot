import io
import json

from aiogram import types

from utils.secondary_functions.get_filepath import get_json_filepath


async def write_json_file(message: types.Message, *, data: object = None, name: str = "") -> None:
    """Запись данных в json
    """
    path  = await get_json_filepath(message, name)
    name_path = path + name

    try:
        with io.open(name_path + '.json', 'w', encoding='utf8') as outfile:
            str_ = json.dumps(data,
                              indent=4,
                              sort_keys=True,
                              separators=(',', ': '),
                              ensure_ascii=False)
            outfile.write(str_)
    except TypeError as err:
        print(f" TypeError: {repr(err)}")
