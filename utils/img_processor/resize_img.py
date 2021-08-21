
from PIL import Image
from io import BytesIO

# from utils.generate_report.generator_report import MAXIMUM_ROW_HEIGHT


async def resize_img(url, size=(100, 100)):

    img = Image.open(url)

    h, w = img.size
    scale = 120 / max(h, w)
    img.resize((int(h * scale), int(w * scale)), Image.ANTIALIAS)


    # if size:
    #     img = img.resize(size)
    temp = BytesIO()
    img.save(temp, format="png")
    temp.seek(0)
    return Image.open(temp)


