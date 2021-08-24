
from openpyxl.styles import Font


async def set_font(ws):

    for row in ws.iter_rows():
        for cell in row:
            cell.font = Font(size=14)
