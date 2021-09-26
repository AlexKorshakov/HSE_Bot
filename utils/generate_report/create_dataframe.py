from typing import Optional

from loguru import logger
from pandas import DataFrame

from utils.json_worker.read_json_file import read_json_file


async def create_dataframe_from_data(data) -> Optional[DataFrame]:
    """Создание dataframe из списка файлов file_list
    :param data:
    :return:
    """

    column_list = [
        "violation_id",
        "main_category",
        "category",
        "violation_category",
        "general_contractor",
        "description",
        "comment",
        "incident_level",
        "elimination_time",
        "act_required",
        "coordinates",
    ]
    try:
        dataframe = DataFrame(data, columns=column_list)
        return dataframe
    except Exception as err:
        logger.error(f"get_workbook {repr(err)}")
        return None


async def create_dataframe(file_list) -> Optional[DataFrame]:
    data = [
        {
            "violation_id": "id записи",
            "main_category": "Основное направление",
            "category": "Категория нарушения",
            "violation_category": "Категория нарушений",
            "general_contractor": "Подрядная организация",
            "description": "Описание нарушения",
            "comment": "Комментарий",
            "incident_level": "Уровень происшествия",
            "elimination_time": "Дней на устранение",
            "act_required": "Оформление акта",
            "coordinates": "Координаты",
        }
    ]

    for file in file_list:
        data.append(await read_json_file(file))

    column_list = [
        "violation_id",
        "main_category",
        "category",
        "violation_category",
        "general_contractor",
        "description",
        "comment",
        "incident_level",
        "elimination_time",
        "act_required",
        "coordinates",
    ]

    try:
        dataframe = DataFrame(data, columns=column_list)
        return dataframe
    except Exception as err:
        logger.error(F"create_dataframe {repr(err)}")
        return None
