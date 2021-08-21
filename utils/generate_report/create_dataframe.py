

import pandas as pd

from utils.json_handler.read_json_file import read_json_file


async def create_dataframe(file_list):


    data = [{
        "main_category": "Основное направление",
        "category": "Категория нарушения",
        "violation_category": "Категория нарушений",
        "general_contractor": "Подрядная организация",
        "description": "Описание нарушения",
        "comment": "Комментарий",
        "latitude": "Широта",
        "longitude": "Долгота"
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
        "latitude",
        "longitude",
    ]

    df = pd.DataFrame(data, columns=column_list)

    return df