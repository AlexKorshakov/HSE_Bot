import io
import json


async def write_json_file(*, data: object = None, name: str = "") -> None:
    """Запись данных в json
    """
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