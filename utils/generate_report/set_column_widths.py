import openpyxl

from utils.generate_report.xlsx_config import MAXIMUM_COLUMN_WIDTH


async def set_column_widths(worksheet):
    """
    """
    for column_cells in worksheet.columns:
        column_length = max(len(_as_text(cell.value)) for cell in column_cells)

        if column_length < MAXIMUM_COLUMN_WIDTH:
            new_column_length = column_length
        else:
            new_column_length = MAXIMUM_COLUMN_WIDTH

        new_column_letter = (openpyxl.utils.get_column_letter(column_cells[0].column))
        if new_column_length > 0:
            worksheet.column_dimensions[new_column_letter].width = new_column_length + 1


def _as_text(value) -> str:
    """
    """
    if value is None:
        return ""
    return str(value)