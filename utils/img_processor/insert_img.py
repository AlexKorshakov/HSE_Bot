import openpyxl
from openpyxl.drawing.image import Image
from utils.json_handler.read_json_file import read_json_file


async def insert_img(json_data, worksheet):
    """
    """
    for ind, j_data in enumerate(json_data, start=2):
        img_data = await read_json_file(j_data)
        img = openpyxl.drawing.image.Image(img_data['filepath'])

        img.height = 160 # высота

        scale = img.height / max(img.height, img.width)

        img.width  = img.width * scale # ширина

        img.anchor = str('L' + str(ind))

        worksheet.add_image(img)