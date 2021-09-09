from typing import Optional

import pandas as pd
from pandas import DataFrame

from utils.json_worker.read_json_file import read_json_file


async def create_dataframe_from_data(data) -> Optional[DataFrame]:
    """Создание dataframe из списка файлов file_list
    :param data:
    :return:
    """

    column_list = ["main_category",
                   "category",
                   "violation_category",
                   "general_contractor",
                   "description",
                   "comment",
                   "report",
                   "coordinates",
                   ]
    try:
        dataframe = pd.DataFrame(data, columns=column_list)
        return dataframe
    except Exception as err:
        print(F"get_workbook {repr(err)}")
        return None


async def create_dataframe(file_list) -> Optional[DataFrame]:
    data = [{
        "main_category": "Основное направление",
        "category": "Категория нарушения",
        "violation_category": "Категория нарушений",
        "general_contractor": "Подрядная организация",
        "description": "Описание нарушения",
        "comment": "Комментарий",
        "report": "Акт?",
        "coordinates": "Координаты",
    }]

    for index, file in enumerate(file_list):
        data.append(await read_json_file(file))

    column_list = [
        "main_category",
        "category",
        "violation_category",
        "general_contractor",
        "description",
        "comment",
        "report",
        "coordinates",
    ]

    try:
        dataframe = pd.DataFrame(data, columns=column_list)
        return dataframe
    except Exception as err:
        print(F"get_workbook {repr(err)}")
        return None
