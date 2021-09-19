from loguru import logger
import openpyxl.utils
from utils.generate_report.xlsx_config import MAXIMUM_COLUMN_WIDTH


async def set_column_widths(worksheet):
    """Форматирование ячейки: ширина столбца
    """

    for column_cells in worksheet.columns:
        # максимальная ширина столбца
        column_length = max(len(_as_text(cell.value)) for cell in column_cells)

        if column_length < MAXIMUM_COLUMN_WIDTH:
            new_column_length = column_length
        else:
            new_column_length = MAXIMUM_COLUMN_WIDTH

        new_column_letter: int = (openpyxl.utils.get_column_letter(column_cells[0].column))
        if new_column_length > 0:
            try:
                worksheet.column_dimensions[new_column_letter].width = new_column_length + 1
            except Exception as err:
                logger.error(f"set_column_widths {repr(err)}")


def _as_text(value) -> str:
    """Приведение данных к str
    """
    if value is None:
        return ""
    return str(value)
