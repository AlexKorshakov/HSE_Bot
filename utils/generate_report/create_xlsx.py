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
