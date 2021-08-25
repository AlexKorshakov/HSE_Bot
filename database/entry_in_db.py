from data.report_data import global_reg_form
from utils.json_handler.writer_json_file import write_global_json_file


async def entry_in_db(*,reg_data):
    global_reg_form[reg_data["user_id"]] = reg_data

    await write_global_json_file(data = global_reg_form)