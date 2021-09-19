import openpyxl
from loguru import logger

from utils.generate_report.xlsx_config import STARTROW, STARTCOL


async def create_xlsx(dataframe, report_file):
    """Создание xlsx из dataframe
    """
    try:
        dataframe.to_excel(report_file, header=False, startrow=STARTROW, startcol=STARTCOL)
        return True
    except Exception as err:
        logger.error(F"set_border {repr(err)}")
        return None


async def create_new_xlsx(report_file):
    """Создание xlsx
    """
    try:
        wb = openpyxl.Workbook()
        wb.save(report_file)
        return True
    except Exception as err:
        logger.error(F"set_border {repr(err)}")
        return None
