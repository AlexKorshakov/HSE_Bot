import json
from json import JSONDecodeError

import inspect, os.path

filename = inspect.getframeinfo(inspect.currentframe()).filename
path = os.path.dirname(os.path.abspath(filename))

MAIN_CATEGORY_LIST: list[str] = [
    "Охрана труда",
    "Промышленная безопасность",
    "Пожарная безопасность",
    "Экология",
    "БДД",
    "ГО и ЧС"
]

CATEGORY_LIST: list[str] = [
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

VIOLATION_CATEGORY: list[str] = [
    "Происшествие без последствий*",
    "Опасные действия*",
    "Травма*",
    "Опасная ситуация*",
    "FAT*",
    "LTI*",
    "Акт-предписание*",
    "акт 2го уровня*"
]

GENERAL_CONTRACTORS: list[str] = [
    "Строй-Монтаж 2002(?)",
    "МИП - Строй 1(?)",
    "СиАрСиСи Рус(?)",
    "ГорИнжПроект(?)",
    "Прочее(?)"
]


def get_names_from_json(name=None):
    """ Функция получения настроек из файла json.
    """
    if name:
        try:
            with open(path + "\\" + name + ".json", "r", encoding="UTF-8") as read_file:
                return json.loads(read_file.read())

        except FileNotFoundError as err:
            print(f"{repr(err)}")
        except JSONDecodeError as err:
            print(f"{repr(err)}")
        except Exception as err:
            print(f"{repr(err)}")
