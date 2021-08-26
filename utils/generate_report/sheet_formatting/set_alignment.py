from openpyxl.styles import Alignment


async def set_alignment(ws):
    """Форматирование ячейки: положение текста в ячейке (лево верх)
    """
    wrap_alignment = Alignment(wrap_text=True, horizontal='left', vertical='center')

    for row in ws.iter_rows():
        for cell in row:
            try:
                cell.alignment = wrap_alignment
            except Exception as err:
                print(F"set_alignment {repr(err)}")
