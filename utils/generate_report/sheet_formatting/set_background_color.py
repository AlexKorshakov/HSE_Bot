from loguru import logger
from openpyxl.styles import PatternFill


async def set_background_color(worksheet, cell_range, rgb='FF7030A0'):
    """Установка цвета заливки ячейки
    :return:
    """
    rows = worksheet[cell_range]
    for row in rows:
        for cell in row:
            try:
                color_fill = PatternFill(start_color=rgb,
                                         end_color=rgb,
                                         fill_type='solid')
                cell.fill = color_fill
            except Exception as err:
                logger.error(f"set_border {repr(err)}")
