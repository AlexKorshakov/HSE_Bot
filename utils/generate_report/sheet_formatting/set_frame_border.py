from loguru import logger
from openpyxl.styles import Border, Side


async def set_border(worksheet):
    """Форматирование ячейки: все границы ячейки
    """
    thin_border = Border(left=Side(style='thin'),
                         right=Side(style='thin'),
                         top=Side(style='thin'),
                         bottom=Side(style='thin'))

    for row in worksheet.iter_rows():
        for cell in row:
            try:
                cell.border = thin_border
            except Exception as err:
                logger.error(f"set_border {repr(err)}")


async def set_range_border(worksheet, cell_range):
    """Форматирование ячейки: все границы ячейки
    """
    thin_border = Border(left=Side(style='thin'),
                         right=Side(style='thin'),
                         top=Side(style='thin'),
                         bottom=Side(style='thin'))

    rows = worksheet[cell_range]
    for row in rows:
        for cell in row:
            try:
                cell.border = thin_border
            except Exception as err:
                logger.error(f"set_border {repr(err)}")
