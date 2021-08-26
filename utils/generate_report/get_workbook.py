from typing import Optional

import openpyxl
from openpyxl import Workbook


async def get_workbook(fill_report_path: str) -> Optional[Workbook]:
    """Открыть и загрузить Workbook
    :param fill_report_path: str полный путь к файлу
    :return: Workbook or None
    """
    try:
        workbook: Workbook = openpyxl.load_workbook(fill_report_path)
        return workbook
    except Exception as err:
        print(F"get_workbook {repr(err)}")
        return None
