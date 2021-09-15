import inspect
import json
import os.path
from json import JSONDecodeError

from loguru import logger

filename = inspect.getframeinfo(inspect.currentframe()).filename
path = os.path.dirname(os.path.abspath(filename))

MAIN_CATEGORY_LIST: list = [
    "Охрана труда",
    "Промышленная безопасность",
    "Пожарная безопасность",
    "Экология",
    "БДД",
    "ГО и ЧС",
]

CATEGORY_LIST: list = [
    'Охрана труда_',
    'Промышленная безопасность_',
    'Экология_',
    'Пожарная безопасность_',
    'Земляные работы_',
    'Работы на высоте_',
    'Работы в замкнутом пространстве_',
    'Огневые работы_',
    'Погрузо-разгрузочные работы_',
    'Безопасность дорожного движения_',
    'Электробезопасность_',
    'Работа без наряд-допусков_',
    'Документация_',
    'Не безопасное поведение_',
    'Не безопасное состояние',
    'Обучения и инструктажи_',
    'Курение в неположенном месте_',
    'Складирование материалов ГСМ_',
    'Сокрытие обстоятельств НС_',
]

VIOLATION_CATEGORY: list = [
    "Опасные действия*",
    "RWC (Ограниченный рабочий случай)",
    "Опасная ситуация*",
    "NearMiss (Происшествие без последствий)",
    "FAT (со смертельным исходом)",
    "LTI (травма с врем. потерей трудоспособности)",
    "Лёгкий НС",
    "RTA (дорожно-транспортное происшествие)",
    "Тяжелый и групповой НС"
]

GENERAL_CONTRACTORS: list = [
    "Строй-Монтаж 2002(?)",
    "МИП - Строй 1(?)",
    "СиАрСиСи Рус(?)",
    "ГорИнжПроект(?)",
    "Прочее(?)"
]

ACT_REQUIRED_ACTION: list = [
    "Требуется*",
    "Не требуется",
]

INCIDENT_LEVEL: list = [
    'Без последствий',
    'Лёгкий',
    'Серьезный',
    'Катастрофический',
]


def get_names_from_json(name=None):
    """ Функция получения настроек из файла json.
    """
    if name:
        try:
            with open(path + "\\" + name + ".json", "r", encoding="UTF-8") as read_file:
                return json.loads(read_file.read())

        except FileNotFoundError as err:
            logger.error(f"{repr(err)}")
        except JSONDecodeError as err:
            logger.error(f"{repr(err)}")
        except Exception as err:
            logger.error(f"{repr(err)}")
