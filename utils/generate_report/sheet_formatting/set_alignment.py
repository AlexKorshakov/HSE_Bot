from loguru import logger
from openpyxl.styles import Alignment


async def set_alignment(worksheet):
    """Форматирование ячейки: положение текста в ячейке (лево верх)
    """
    wrap_alignment = Alignment(wrap_text=True, horizontal='left', vertical='center')

    for row in worksheet.iter_rows():
        for cell in row:
            try:
                cell.alignment = wrap_alignment
            except Exception as err:
                logger.error(f"set_alignment {repr(err)}")


async def set_mip_alignment(worksheet, cell_range, horizontal=None, vertical=None):
    """Форматирование ячейки: положение текста в ячейке (лево верх)
    """
    wrap_alignment = Alignment(wrap_text=True, horizontal=horizontal, vertical=vertical)

    cells = [cell for row in worksheet[cell_range] for cell in row]

    for item, cell in enumerate(cells, start=1):
        try:
            cell.alignment = wrap_alignment
        except Exception as err:
            logger.error(f"iter {item} cell {cell}")
            logger.error(f"set_mip_alignment {repr(err)}")
