from utils.generate_report.xlsx_config import STARTROW, STARTCOL


async def create_xlsx(df, report_file):
    """Создание xlsx из dataframe
    """
    try:
        df.to_excel(report_file, header=False, startrow=STARTROW, startcol=STARTCOL)
        return True
    except Exception as err:
        print(F"set_border {repr(err)}")
        return  None
