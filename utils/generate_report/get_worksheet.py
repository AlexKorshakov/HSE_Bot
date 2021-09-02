from typing import Optional

from openpyxl import Workbook
from xlsxwriter.worksheet import Worksheet


async def get_worksheet(wb: Workbook, index: int = 0)-> Optional[Worksheet]:
    """Получение Страницы из документа по индексу
    :param wb: Workbook - книга xls
    :param index: int - индекс листа
    :return: worksheet or None
    """
    try:
        worksheet: Worksheet = wb.worksheets[index]
        return worksheet
    except Exception as err:
        print(f"get_workbook {repr(err)}")
        return None
