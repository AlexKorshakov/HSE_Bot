import os.path

import openpyxl
from loguru import logger
from openpyxl.drawing.image import Image
from xlsxwriter.worksheet import Worksheet

from data.config import WORK_PATH
from utils.secondary_functions.get_json_files import get_files

from utils.json_worker.read_json_file import read_json_file

COLUMN_STR_INDEX: str = 'O'
SIGNALLINE_COLUMN_STR_INDEX: str = "B"

IMG_ANCHOR = True
IMG_SCALE = True


async def insert_images_to_sheet(json_data, worksheet: Worksheet, height=160):
    """Вставка изображения в лист worksheet
    """
    for ind, j_data in enumerate(json_data, start=2):
        try:
            img_data = await read_json_file(j_data)

            img: Image = openpyxl.drawing.image.Image(img_data['photo_full_name'])

            if img is None:
                logger.error(f"Изображение для вставки в строку {ind} не найдено!")
                continue

            img_params: dict = {
                "height": height,
                "scale": IMG_SCALE,
                "anchor": IMG_ANCHOR,
                "column": COLUMN_STR_INDEX,
                "row": ind
            }

            img = await image_preparation(img, img_params)

            await insert_images(worksheet, img=img)

        except Exception as err:
            logger.error(f"insert_img {repr(err)}")
            return None


async def insert_signalline_to_report_body(worksheet: Worksheet) -> None:
    """
    :param worksheet:
    :return:
    """
    photo_full_name = ".\\signalline.jpeg"

    files = await get_files(main_path=WORK_PATH + "\\utils\\", endswith=".jpg")

    for file in files:
        photo_full_name = file if file.split('\\')[-1].split('.')[0] == "signalline" else ''

    if not os.path.isfile(photo_full_name):
        logger.error("signalline not found")
        return

    img: Image = openpyxl.drawing.image.Image(photo_full_name)

    # height = 0
    # for item in range(3, 42):
    #     height += int(worksheet.row_dimensions[item].height)
    # width = worksheet.column_dimensions[SIGNALLINE_COLUMN_STR_INDEX].width
    # width = 115
    # height = 1552

    img_params: dict = {
        # "width": width * 2.54,
        # "height": height * 2.54,
        # "scale": IMG_SCALE,
        "anchor": IMG_ANCHOR,
        "column": SIGNALLINE_COLUMN_STR_INDEX,
        "row": 4
    }

    img = await image_preparation(img, img_params)

    await insert_images(worksheet, img=img)


async def image_preparation(img: Image, img_params: dict):
    """Подготовка изображения перед вставкой на страницу
    """

    height = img_params.get("height")
    scale = img_params.get("scale")
    width = img_params.get("width")
    anchor = img_params.get("anchor")
    column = img_params.get("column")
    row = img_params.get("row")

    # высота изображения
    if height:
        img.height = height

    # ширина изображения
    if width:
        img.width = width

    # изменение пропорций изображения
    if scale:
        scale = img.height / max(img.height, img.width)
        img.width = img.width * scale

    # прикрепление изображение по адресу str(column) + str(row)
    if anchor:
        img.anchor = str(column) + str(row)

    return img


async def insert_images(worksheet: Worksheet, img: Image):
    """Вставка изображения на лист worksheet*,
    :param img: файл изображения
    :param worksheet: Worksheet - страница документа для вставки изображения
    :return:
    """

    try:
        worksheet.add_image(img)
    except Exception as err:
        logger.error(f"insert_images {repr(err)}")
        return None
