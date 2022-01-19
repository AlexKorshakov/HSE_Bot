import os
import subprocess
import time
from pprint import pprint

import git
from psutil import Process, NoSuchProcess
from git import Repo, RemoteProgress
from loguru import logger
from tqdm import tqdm

DELAY = 60


def start_bot():
    """Запуск процесса бота из .bat"""
    proc = subprocess.Popen(f"HSE_Bot.run.bat", creationflags=subprocess.CREATE_NEW_CONSOLE)
    return proc


def kill_bot(proc):
    """Остановка процесса бота и всех дочерних процессов"""
    pobj = Process(proc.pid)

    try:
        for children in pobj.children(recursive=True):  # list children & kill them
            try:
                children.kill()
                pprint(f'{children = }')
            except NoSuchProcess:
                logger.info(f'NoSuchProcess')

        pobj.kill()
        logger.info(f'all children processes kill')

    except Exception as err:
        logger.error(f'{repr(err)}')
        logger.info(f"taskkill /f /im HSE_Bot.run.bat")


class PullProgress(RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        pbar = tqdm(total=max_count)
        pbar.update(cur_count)


def get_update_from_git(repo) -> bool:
    """Поиск обновлений в ветке master репозитория на githab"""

    diff_tree = repo.git.execute(['git', 'diff-tree', '--name-status', '-t', 'master', 'origin/master'])

    if diff_tree:
        for line in diff_tree.splitlines():  # type: ignore
            change_status, file_path = line.split('\t')
            logger.info(f'{change_status = } : {file_path = }')

        logger.info(f'received updates from the repository')
        return True
    return False


def update_repo():
    """Обновлений репозитория с Git"""

    # repo.git.execute(['git', 'remote', 'prune', 'origin'])
    # repo.git.execute(['git', 'update-ref', '-d', 'refs/remotes/origin/master'])
    # repo.git.execute(['git', 'remote', 'add', 'origin', 'https://github.com/AlexKorshakov/HSE_Bot/'])
    # repo.remote().pull(['git', 'pull', '-v', 'origin', 'master', "merge"])
    # repo.git.execute(['git', 'pull', '-v', 'origin', 'master', "merge"])
    # repo.remotes.origin.pull('master')

    git.cmd.Git().pull('https://github.com/AlexKorshakov/HSE_Bot', 'master', '--rebase[merges]', '--autostash')
    # git.cmd.Git().fetch('--all')
    # git.cmd.Git().branch('backup-master')
    # git.cmd.Git().reset('--hard', 'origin/master')


def reload():
    global prog

    path = os.path.abspath(os.curdir)
    repo = Repo(path)

    try:
        while True:
            prog = start_bot()
            time.sleep(DELAY)

            if get_update_from_git(repo):
                kill_bot(prog)
                update_repo()

            kill_bot(prog)

    except Exception:
        kill_bot(prog)
        reload()
    finally:
        kill_bot(prog)


if __name__ == '__main__':
    reload()
