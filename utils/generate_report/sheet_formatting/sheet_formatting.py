from loguru import logger
from xlsxwriter.worksheet import Worksheet

from utils.generate_report.mip_report_settings import RANGE_COLUMNS, MERGED_CELLS, ROW_DIMENSIONS, CELL_RANGES, \
    CELL_RANGE_BACKGROUND_COLOR, CELL_RANGES_ALIGNMENT, CELL_RANGES_BASIC_ALIGNMENT, CELL_RANGES_SET_REPORT_FONT
from utils.generate_report.sheet_formatting.set_alignment import set_alignment, set_mip_alignment
from utils.generate_report.sheet_formatting.set_background_color import set_background_color
from utils.generate_report.sheet_formatting.set_column_widths import set_column_widths
from utils.generate_report.sheet_formatting.set_font import set_font, set_report_font, sets_report_font
from utils.generate_report.sheet_formatting.set_frame_border import set_border, set_range_border
from utils.generate_report.sheet_formatting.set_row_height import set_row_height


async def format_sheets(worksheet: Worksheet):
    """Пошаговое форматирование страницы
    """

    await set_border(worksheet)
    await set_alignment(worksheet)
    await set_font(worksheet)
    await set_column_widths(worksheet)
    await set_row_height(worksheet)


async def format_mip_report_sheet(worksheet: Worksheet):
    """Пошаговое форматирование страницы
    """

    for item in RANGE_COLUMNS:

        try:
            worksheet.column_dimensions[item[0]].width = item[1]
        except Exception as err:
            logger.error(f"set_column_widths {repr(err)}")

    worksheet.print_title_rows = '$2:$3'
    worksheet.print_title = '$2:$3'

    worksheet.print_options.horizontalCentered = True

    worksheet.print_area = '$A$1:$I$48'

    for merged_cell in MERGED_CELLS:
        worksheet.merge_cells(merged_cell)

    await set_range_border(worksheet, cell_range=CELL_RANGES)

    for item in ROW_DIMENSIONS:
        worksheet.row_dimensions[int(item[0])].height = float(item[1])

    for item, cell_range in enumerate(CELL_RANGES_BASIC_ALIGNMENT, start=1):
        await set_report_font(worksheet, cell_range=cell_range, font_size=14)

    for item in CELL_RANGE_BACKGROUND_COLOR:
        await set_background_color(worksheet, item[0], rgb=item[1])

    for item, cell_range in enumerate(CELL_RANGES_BASIC_ALIGNMENT, start=1):
        await set_mip_alignment(worksheet, cell_range, horizontal='left', vertical='center')

    for item, cell_range in enumerate(CELL_RANGES_ALIGNMENT, start=1):
        await set_mip_alignment(worksheet, cell_range, horizontal='center', vertical='center')

    for item, cell_range in enumerate(CELL_RANGES_SET_REPORT_FONT, start=1):
        await sets_report_font(worksheet, cell_range[0], params=cell_range[1])
