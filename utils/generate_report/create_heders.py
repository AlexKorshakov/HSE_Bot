from utils.json_worker.read_json_file import read_json_file


async def create_heders(file_list=None):
    """Подготовка заголовков таблицы отчета
    :param file_list:
    :return:
    """
    data = [{"main_category": "Основное направление",
             "category": "Категория нарушения",
             "violation_category": "Категория нарушений",
             "general_contractor": "Подрядная организация",
             "description": "Описание нарушения",
             "comment": "Комментарий",
             "incident_level": "Уровень происшествия",
             "act_required": "Оформление акта",
             "coordinates": "Координаты",
             }]

    return data
