from openpyxl.styles import Border, Side


async def set_border(ws):
    """Форматирование ячейки: все границы ячейки
    """
    thin_border = Border(left=Side(style='thin'),
                         right=Side(style='thin'),
                         top=Side(style='thin'),
                         bottom=Side(style='thin'))

    for row in ws.iter_rows():
        for cell in row:
            try:
                cell.border = thin_border
            except Exception as err:
                print(F"set_border {repr(err)}")