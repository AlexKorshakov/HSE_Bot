async def merge_json(json_list) -> list:
    """Обьединение json в один файл
    """
    merged_json = []
    for item in json_list:
        merged_json.append(item)

    return merged_json


async def merge_json_day_report(json_list):
    """Обьединение json в один файл
    """
    return [item for item in json_list]
