import io
import json

from loguru import logger

from data.config import BOT_DATA_PATH

SUFFIX: str = ".json"


async def write_json_file(*, data: object = None, name: str = "") -> None:
    """Запись данных в json
    """
    await write_json(name=name, data=data)


async def write_json_reg_user_file(*, data: dict = None) -> bool:
    """Запись данных в json
    """
    name = data['reg_json_full_name']

    # if not os.path.isfile(name):
    # Todo: check

    await write_json(name=name, data=data)
    return True


async def write_json_violation_user_file(*, data: dict = None) -> bool:
    """Запись данных о нарушениях в json
    """
    name = str(data["json_full_name"])

    await write_json(name=name, data=data)
    return True


async def write_global_json_file(*, data: dict = None) -> None:
    """Запись регистрацтонных данных в json
    """
    name = BOT_DATA_PATH + "registration_db" + SUFFIX

    await write_json(name=name, data=data)


async def write_json(name, data):
    """Запись данных в json
    :param name:
    :param data:
    :return:
    """
    try:
        with io.open(name, 'w', encoding='utf8') as outfile:
            str_ = json.dumps(data,
                              indent=4,
                              sort_keys=True,
                              separators=(',', ': '),
                              ensure_ascii=False)
            outfile.write(str_)
    except TypeError as err:
        logger.error(f" TypeError: {repr(err)}")
