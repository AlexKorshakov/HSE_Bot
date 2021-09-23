from openpyxl.worksheet.pagebreak import Break


async def set_page_setup(worksheet):
    """Установка параметров страницы
    :param worksheet:
    :return:
    """

    #  https://xlsxwriter.readthedocs.io/page_setup.html
    worksheet.print_title_rows = '$2:$3'
    worksheet.print_title = '$2:$3'

    # Printer Settings
    worksheet.page_setup.orientation = worksheet.ORIENTATION_PORTRAIT
    worksheet.page_setup.paperSize = worksheet.PAPERSIZE_A4

    # Подогнать область печати к определенному кол-у страниц как по вертикали, так и по горизонтали.
    worksheet.page_setup.fitToPage = True
    worksheet.page_setup.fitToHeight = '0'

    # worksheet.views
    worksheet.print_options.horizontalCentered = True
    worksheet.print_area = '$A$1:$I$48'

    #  масштабный коэффициент для распечатываемой страницы
    # worksheet.set_print_scale(75)

    worksheet.row_breaks.append(Break(id=45))
    worksheet.col_breaks.append(Break(id=9))
