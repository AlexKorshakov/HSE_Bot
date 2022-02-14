import time

from aiogram import types
from loguru import logger

from loader import bot
from messages.messages import Messages
from win32com import client


async def close_excel_by_force(excel):
    """Принудительное закрытие Excel  после окончания работы
    :param excel:
    :return:
    """
    import win32process
    import win32gui
    import win32api
    import win32con

    # Get the window's process id's
    hwnd = excel.Hwnd
    t, p = win32process.GetWindowThreadProcessId(hwnd)
    # Ask window nicely to close
    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
    # Allow some time for app to close
    time.sleep(10)
    # If the application didn't close, force close
    try:
        handle = win32api.OpenProcess(win32con.PROCESS_TERMINATE, 0, p)
        if handle:
            win32api.TerminateProcess(handle, 0)
            win32api.CloseHandle(handle)
    except Exception as err:
        logger.warning(repr(err))


async def convert_xlsx_to_pdf(*, path: str) -> bool:
    """Конвертация эксель файла в pdf
    """
    if not path:
        return False

    input_file = path
    # give your file name with valid path
    output_file = path.replace('.xlsx', '.pdf')
    # give valid output file name and path
    app = client.DispatchEx("Excel.Application")
    app.Interactive = False
    app.Visible = False
    workbook = app.Workbooks.Open(input_file)
    try:
        workbook.ActiveSheet.ExportAsFixedFormat(0, output_file)
        return True
    except Exception as err:
        logger.warning(
            "Failed to convert in PDF format.Please confirm environment meets all the requirements and try again")
        logger.warning(repr(err))
    finally:
        workbook.Close()
        await close_excel_by_force(app)  # <--- YOU #@#$# DIEEEEE!! DIEEEE!!!


async def convert_report_to_pdf(chat_id, path: str):
    """Конвертация отчета в pdf
    :param chat_id:
    :param path:
    :return:
    """

    if not await convert_xlsx_to_pdf(path=path):
        await bot.send_message(chat_id=chat_id, text=f'{Messages.Report.error} \n')
    await bot.send_message(chat_id=chat_id, text=f'{Messages.Report.convert_successfully} \n')


if __name__ == '__main__':
    SOURCE_DIR = '\\user_data\\373084462\\data_file\\30.09.2021' \
                 '\\reports\\ЛО-МИП-УОТиПБ НС-стм. Аминьевская 30.09.2021.xlsx'

    convert_xlsx_to_pdf(path=SOURCE_DIR)
