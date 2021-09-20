from loguru import logger
from openpyxl.styles import Font


async def set_font(ws):
    """Форматирование ячейки: размер шрифта
    """
    for row in ws.iter_rows():
        for cell in row:
            try:
                cell.font = Font(size=14)
            except Exception as err:
                logger.error(f"sets_report_font {repr(err)}")


async def set_report_font(worksheet, cell_range, font_size=14, name='Arial', color=""):
    """Форматирование ячейки: размер шрифта
    """
    cells = [cell for row in worksheet[cell_range] for cell in row]

    for item, cell in enumerate(cells, start=1):
        try:

            cell.font = Font(size=font_size, name=name)

        except Exception as err:
            logger.error(f"item {item} cell {cell}")
            logger.error(f"set_report_font {repr(err)}")


async def sets_report_font(worksheet, cell_range, params: dict):
    """Форматирование ячейки: размер шрифта
    """
    cells = [cell for row in worksheet[cell_range] for cell in row]

    for item, cell in enumerate(cells, start=1):
        try:
            cell.font = Font(
                color=params.get("color"),
                italic=params.get("italic"),
                size=params.get("font_size"),
                bold=params.get("bold"),
                name=params.get("name"),
                underline=params.get("underline"),
                vertAlign=params.get("vertAlign"),
            )

        except Exception as err:
            logger.error(f"item {item} cell {cell}")
            logger.error(f"sets_report_font {repr(err)}")
