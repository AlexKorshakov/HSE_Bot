from utils.generate_report.xlsx_config import MAXIMUM_ROW_HEIGHT


async def set_row_height(worksheet):
    """
    """
    for ind in range(worksheet.max_row):
        if ind == 0:
            continue
        worksheet.row_dimensions[ind + 1].height = MAXIMUM_ROW_HEIGHT