import io
import json

from data.config import BOT_DATA_PATH


async def write_json(name, data):
    try:
        with io.open(name, 'w', encoding='utf8') as outfile:
            str_ = json.dumps(data,
                              indent=4,
                              sort_keys=True,
                              separators=(',', ': '),
                              ensure_ascii=False)
            outfile.write(str_)
    except TypeError as err:
        print(f" TypeError: {repr(err)}")


async def write_json_file(*, data: object = None, name: str = "") -> None:
    """Запись данных в json
    """
    await write_json(name=name, data=data)


async def write_json_reg_user_file(*, data: dict = None) -> None:
    """Запись данных в json
    """
    name = data['reg_user_file'] + '\\' + data['user_id']

    await write_json(name=name, data=data)


async def write_global_json_file(*, data: dict = None) -> None:
    """Запись данных в json
    """

    name = BOT_DATA_PATH + "registration_db"

    await write_json(name=name, data=data)
