
from openpyxl.styles import Font


async def set_font(ws):
    """Форматирование ячейки: размер шрифта
    """
    for row in ws.iter_rows():
        for cell in row:
            try:
                cell.font = Font(size=14)
            except Exception as err:
                print(F"set_border {repr(err)}")