import os
from types import ModuleType
from importlib import reload

from aiogram import types
from aiogram.dispatcher.filters import Command
from config import logger

from data.config import WORK_PATH
from loader import dp


@dp.message_handler(Command('reload'))
async def reload_handler(message: types.Message):
    subfolders, files = run_fast_scandir(WORK_PATH, [".py"])
    modules_path = [file for file in files if not "venv" in file]

    moduls = [str(mod.replace(WORK_PATH, '').split(".")[0][1:].replace("\\", '.')) for mod in modules_path]

    for modul, module_path in zip(moduls, modules_path):

        module_spec = check_module(modul)
        module = importlib.import_module(modul, package=module_path)
        importlib.reload(module)

        if module_spec:
            module = import_module_from_spec(module_spec)
            logger.info(dir(module))


def run_fast_scandir(dir, ext):
    subfolders, files = [], []

    for file in os.scandir(dir):
        if file.is_dir():
            subfolders.append(file.path)
        if file.is_file():
            if os.path.splitext(file.name)[1].lower() in ext:
                files.append(file.path)

    for dir in list(subfolders):
        sf, file = run_fast_scandir(dir, ext)
        subfolders.extend(sf)
        files.extend(file)

    return subfolders, files


class ReloadModule:
    """ Класс для перезагрузки указанного модуля.
    """

    def __init__(self, *, module, module_path):
        self.module = module
        self.path = module_path

    def get_reload(self) -> None:
        """ Порядок презагрузки.
        """

        if not self.module or not isinstance(self.module, ModuleType):
            raise TypeError("reload() argument must be a module")
        self._reload_module()

    def _reload_module(self) -> None:
        """ Функция перезагрузки указанного модуля.
        """
        try:
            reload(self.module)
        except FileNotFoundError:
            return


import importlib.util


def check_module(module_name):
    """
    Проверяет, можно ли импортировать модуль без его фактического импорта
    """
    module_spec = importlib.util.find_spec(module_name)
    if module_spec is None:
        logger.error('Module: {} not found'.format(module_name))
        return None
    else:
        logger.info('Module: {} can be imported!'.format(module_name))
        return module_spec


def import_module_from_spec(module_spec):
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)

    return module

# if __name__ == '__main__':
#     module_spec = check_module('fake_module')
#     module_spec = check_module('collections')
#
#     if module_spec:
#         module = import_module_from_spec(module_spec)
#         print(dir(module))
