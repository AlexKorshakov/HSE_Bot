import openpyxl
from openpyxl.drawing.image import Image
from xlsxwriter.worksheet import Worksheet

from utils.generate_report.xlsx_config import COLUMN_SRT_INDEX
from utils.json_handler.read_json_file import read_json_file


async def insert_images_too_sheet(json_data, worksheet: Worksheet):
    """Вставка изображения в лист worksheet
    """
    for ind, j_data in enumerate(json_data, start=2):
        try:
            img_data = await read_json_file(j_data)
            img: Image = openpyxl.drawing.image.Image(img_data['filepath'])

            await insert_images(img, ind, worksheet)
        except Exception as err:
            print(F"insert_img {repr(err)}")
            return None


async def insert_images(img: Image, ind:int, worksheet: Worksheet):
    """Вставка изображения на лист worksheet
    :param img: файл изображения
    :param ind: int индекс строки для вставки изображения
    :param worksheet: Worksheet - страница документа для вставки изображения
    :return:
    """
    img.height = 160  # высота изображения
    scale = img.height / max(img.height, img.width)
    img.width = img.width * scale  # ширина изображения
    img.anchor = str(COLUMN_SRT_INDEX + str(ind))
    try:
        worksheet.add_image(img)
    except Exception as err:
        print(F"insert_images {repr(err)}")
        return None
