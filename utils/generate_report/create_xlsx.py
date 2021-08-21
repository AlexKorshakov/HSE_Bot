from utils.generate_report.xlsx_config import STARTROW, STARTCOL
import pandas as pd

async def create_xlsx(df, report_file):
    """
    """

    df.to_excel(report_file, header=False, startrow=STARTROW, startcol=STARTCOL)
    #
    # writer = pd.ExcelWriter('pandas_conditional.xlsx', engine='xlsxwriter')
    # df.to_excel(writer, sheet_name='Sheet1')
    #
    #
    # workbook = writer.book
    # worksheet = writer.sheets['Sheet1']
    #
    # pd.set_option()
    return df