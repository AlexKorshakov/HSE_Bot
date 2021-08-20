import io
import json

from utils.secondary_functions.get_filepath import get_json_filepath


async def write_json_file(*, data: object = None, name: str = "") -> None:
    """Запись данных в json
    """
    name= await get_json_filepath(name)

    try:
        with io.open(name + '.json', 'w', encoding='utf8') as outfile:
            str_ = json.dumps(data,
                              indent=4,
                              sort_keys=True,
                              separators=(',', ': '),
                              ensure_ascii=False)
            outfile.write(str_)
    except TypeError as err:
        print(f" TypeError: {repr(err)}")