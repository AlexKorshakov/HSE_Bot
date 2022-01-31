from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.utils.markdown import hlink
from git import Repo, RemoteProgress
from loguru import logger
from tqdm import tqdm

from data.category import get_names_from_json
from data.config import ADMIN_ID, DEVELOPER_ID
from loader import dp, bot


# @rate_limit(limit=20)
# @dp.message_handler(user_id=ADMIN_ID, commands=Command('admin_func'))
@dp.message_handler(Command('admin_func'))
async def admin_func_handler(message: types.Message) -> None:
    """Административные функции
    :param message:
    :return:
    """
    # white_list = await get_names_from_json("white_list")
    black_list = get_names_from_json("black_list")

    if message.from_user.id != int(ADMIN_ID) or message.from_user.id != str(DEVELOPER_ID):
        logger.info(f'User @{message.from_user.username}:{message.from_user.id} looking for a admin_func')
        await message.answer(f'Меня создал {hlink(title="developer", url=f"tg://user?id={ADMIN_ID}")}')

    if message.from_user.id in black_list:
        logger.info(f'User @{message.from_user.username}:{message.from_user.id} попытка доступа в админку!')
        await message.answer(f'у вас нет доступа')

    if message.from_user.id == int(ADMIN_ID) or message.from_user.id == str(DEVELOPER_ID):
        logger.info(f'User @{message.from_user.username}:{message.from_user.id} йа печенько')

        # class PullProgress(RemoteProgress):
        #     def update(self, op_code, cur_count, max_count=None, message=''):
        #         pbar = tqdm(total=max_count)
        #         pbar.update(cur_count)
        #
        # try:
        #     path = 'C:\\Users\\KDeusEx\\PycharmProjects\\HSE_Bot'
        #     repo = Repo(path)
        #     repo.remote().fetch()
        #     repo.remote().pull(progress=PullProgress())
        #
        #     diff_tree = repo.git.execute('git diff-tree --name-status -t master origin/master')
        #
        #     for line in diff_tree.splitlines():  # type: ignore
        #         change_status, file_path = line.split('\t')
        #         logger.info(f'{change_status = }:{file_path = }')
        #
        # except Exception as err:
        #     await message.answer(f'{repr(err)}')

        await message.answer(f' у меня получилось сделать удаленное управление!!')

        return

    await message.answer(f'у вас нет доступа к функциям администратора')
