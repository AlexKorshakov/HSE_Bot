from __future__ import print_function

import asyncio

from loguru import logger

from data.category import get_names_from_json

import moviepy.editor as moviepy

try:
    SENT_TO = get_names_from_json("SENT_TO")
    if SENT_TO is None:
        from data.category import SENT_TO
except Exception as err:
    logger.error(f"{repr(err)}")
    from data.category import SENT_TO


async def send_mail(files: list = None, registration_data: dict = None):
    """Отправка сообщения с отчетом
    :param registration_data:
    :param files:
    :return:
    """
    pass


async def main():


    base_path = 'C:\\Users\\KDeusEx\\Downloads\\[SW.BAND] [Тата Феодориди] Любит-не любит (2021)\\'

    flist = ['Любит-не любит Урок 6.mp4',
             'Любит-не любит Урок 7.mp4']

    for ffail in flist:
        clip = moviepy.VideoFileClip(base_path + ffail)
        clip.write_videofile(base_path + "k_" + ffail, fps=25, codec="mpeg4")
        clip.close()


if __name__ == '__main__':
    asyncio.run(main())
