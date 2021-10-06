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
    "Документы ОТ и ПБ",
    "Обучени, аттестация/квалификация",
    "СИЗ",
    "Механизмы и оборудование",
    "ТС/Спецтехника",
    "Знаки безопасности/ограждения",
    "Земляные работы",
    "Электробезопасность",
    "Бетонные работы",
    "ГПМ",
    "Замкнутые пространства",
    "Ручные инструменты",
    "Работы на высоте",
    "Огневые работы",
    "Оборудование под давлением",
    "Пожарная безопасность",
    "Первая помощь",
    "Химические, биологические факторы",
    "Санитарные требования",
    "Складирование",
    "Безопасные проходы",
    "Отходы",
    "Освещение",
    "Другое"
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

ELIMINATION_TIME: list = [
    "Постоянно",
    "Немедленно",
    "1 день",
    "3 дня",
    "5 дней",
    "7 дней",
    "10 дней",
    "15 дней",
    "21 день",
    "30 дней"
]

SENT_TO: list = [
    "arsutinaa@mosinzhproekt.ru",
    "lozhkov.rd@mosinzhproekt.ru"
]


def get_names_from_json(name=None) -> list:
    """ Функция получения настроек из файла json.
    :return: list
    """
    if name:
        try:
            with open(path + "\\" + name + ".json", "r", encoding="UTF-8") as read_file:
                list_value = json.loads(read_file.read())
                return list_value

        except FileNotFoundError as err:
            logger.error(f"{repr(err)}")
            return []
        except JSONDecodeError as err:
            logger.error(f"{repr(err)}")
            return []
        except Exception as err:
            logger.error(f"{repr(err)}")
            return []
