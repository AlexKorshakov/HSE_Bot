from loguru import logger
from xlsxwriter.worksheet import Worksheet

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
    range_columns = [["A", "3"],
                     ["B", "16"],
                     ["C", "41"],
                     ["D", "6"],
                     ["E", "46"],
                     ["F", "6"],
                     ["G", "30"],
                     ["H", "15"],
                     ["I", "3"]]

    for item in range_columns:

        try:
            worksheet.column_dimensions[item[0]].width = item[1]
        except Exception as err:
            logger.error(f"set_column_widths {repr(err)}")

    worksheet.print_title_rows = '$2:$3'
    worksheet.print_title = '$2:$3'

    worksheet.print_options.horizontalCentered = True

    worksheet.print_area = '$A$1:$I$48'

    merged_cells = ['C43:H43',
                    'C44:H44',
                    'C17:H17',
                    'D18:E18',
                    'C19:C42',
                    'C11:C16',
                    'F11:H11',
                    'F12:H12',
                    'F13:H13',
                    'F14:H14',
                    'F15:H15',
                    'F16:H16',
                    'D6:H6',
                    'D7:H7',
                    'D8:H8',
                    'D9:H9',
                    'D10:E10',
                    'F10:H10',
                    'D2:H2',
                    'D3:E3',
                    'F3:H3',
                    'C4:H4',
                    'D5:H5',
                    ]

    for merged_cell in merged_cells:
        worksheet.merge_cells(merged_cell)

    await set_range_border(worksheet, cell_range='C2:H44')

    row_dimensions = [["2", "39.0"],
                      ["3", "25.8"],
                      ["4", "17.4"],
                      ["5", "17.4"],
                      ["6", "17.4"],
                      ["7", "17.4"],
                      ["8", "17.4"],
                      ["9", "17.4"],
                      ["10", "17.4"],
                      ["11", "24.0"],
                      ["12", "24.0"],
                      ["13", "24.0"],
                      ["14", "24.0"],
                      ["15", "24.0"],
                      ["16", "24.0"],
                      ["17", "17.4"],
                      ["18", "17.4"],
                      ["19", "33.0"],
                      ["20", "33.0"],
                      ["21", "33.0"],
                      ["22", "33.0"],
                      ["23", "33.0"],
                      ["24", "33.0"],
                      ["25", "33.0"],
                      ["26", "33.0"],
                      ["27", "33.0"],
                      ["28", "33.0"],
                      ["29", "33.0"],
                      ["30", "33.0"],
                      ["31", "33.0"],
                      ["32", "33.0"],
                      ["33", "33.0"],
                      ["34", "33.0"],
                      ["35", "33.0"],
                      ["36", "33.0"],
                      ["37", "33.0"],
                      ["38", "33.0"],
                      ["39", "33.0"],
                      ["40", "33.0"],
                      ["41", "33.0"],
                      ["42", "33.0"],
                      ["43", "17.4"],
                      ["44", "58.2"],
                      ["45", "33.0"],
                      ["46", "33.0"],
                      ]

    for item in row_dimensions:

        worksheet.row_dimensions[int(item[0])].height = float(item[1])

    cell_ranges = ['C2:H44']

    for item, cell_range in enumerate(cell_ranges, start=1):

        await set_report_font(worksheet, cell_range=cell_range, font_size=14)

    cell_range = [['C2:H3', "FF7030A0"],
                  ["C5:C16", "FFDCDAFA"],
                  ["D10:H10", "FFDCDAFA"],
                  ["C18:H18", "FFDCDAFA"],
                  ["C19:C42", "FFDCDAFA"],

                  ["C4:H4", "FFFFC000"],
                  ["C17:H17", "FFFFC000"],
                  ["C43:H43", "FFFFC000"],
                  ]

    for item in cell_range:

        await set_background_color(worksheet, item[0], rgb=item[1])

    cell_ranges = ['C2:H44'
                   ]

    for item, cell_range in enumerate(cell_ranges, start=1):

        await set_mip_alignment(worksheet, cell_range, horizontal='left', vertical='center')

    cell_ranges = ["C2:C2",
                   "C3:H3",
                   "C4:H4",
                   "C10:H10",
                   "C17:H17",
                   "C18:H18",
                   "C43:H43",
                   "C44:H44",
                   ]

    for item, cell_range in enumerate(cell_ranges, start=1):

        await set_mip_alignment(worksheet, cell_range, horizontal='center', vertical='center')

    cell_ranges = [["C2:H3", {"color": "FFFFFFFF", "font_size": "14", "bold": "True", "name": "Arial"}],
                   ["C2:C2", {"color": "FFFFFFFF", "font_size": "16", "bold": "True", "name": "Arial"}],
                   ["C4:H4", {"font_size": "14", "bold": "True", "name": "Arial"}],
                   ["C5:H10", {"font_size": "14", "bold": "True", "name": "Arial"}],
                   ["D10:H10", {"font_size": "14", "bold": "True", "italic": "True", "name": "Arial"}],
                   ["D17:H17", {"font_size": "14", "bold": "True", "name": "Arial"}],
                   ["C18:C18", {"font_size": "14", "bold": "True", "name": "Arial"}],
                   ["D18:H18", {"font_size": "14", "bold": "True", "italic": "True", "name": "Arial"}],
                   ["C43:H44", {"font_size": "14", "bold": "True", "name": "Arial"}],
                   ]

    for item, cell_range in enumerate(cell_ranges, start=1):

        await sets_report_font(worksheet, cell_range[0], params=cell_range[1])
