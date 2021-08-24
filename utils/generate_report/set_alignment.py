from openpyxl.styles import Alignment


async def set_alignment(ws):
    wrap_alignment = Alignment(wrap_text=True, horizontal='left', vertical='center')

    for row in ws.iter_rows():
        for cell in row:
            cell.alignment = wrap_alignment
