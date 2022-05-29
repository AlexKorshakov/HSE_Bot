import os.path
import sqlite3
import asyncio

# from database.db import DataBase

from data.config import WORK_PATH
from utils.json_worker.read_json_file import read_json_file
from utils.json_worker.writer_json_file import write_json_file
from utils.secondary_functions.get_json_files import get_files


class DataBase:

    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def create_table(self):
        """Создание таблицы violation"""
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS violations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            
            location VARCHAR NOT NULL,
            work_shift VARCHAR,
            function VARCHAR,
            name VARCHAR NOT NULL,
            parent_id VARCHAR NOT NULL,
            
            violation_id INTEGER,
            user_id INTEGER NOT NULL,
            user_fullname VARCHAR (100),
            report_folder_id VARCHAR (100),
            file_id VARCHAR NOT NULL,
            data VARCHAR NOT NULL,
            day VARCHAR (10) NOT NULL,
            month VARCHAR (10) NOT NULL,
            year VARCHAR (10) NOT NULL,
            now VARCHAR (100) NOT NULL,
            main_category VARCHAR NOT NULL,
            general_contractor VARCHAR NOT NULL,
            category VARCHAR NOT NULL,
            comment VARCHAR NOT NULL,
            act_required VARCHAR NOT NULL,
            description VARCHAR NOT NULL,
            elimination_time VARCHAR NOT NULL,
            incident_level VARCHAR NOT NULL,
            violation_category VARCHAR NOT NULL,
            coordinates VARCHAR DEFAULT (0),
            latitude FLOAT DEFAULT (0),
            longitude FLOAT DEFAULT (0),
            json_folder_id VARCHAR (100) NOT NULL,
            json_file_path VARCHAR,
            json_full_name VARCHAR,
            photo_file_path VARCHAR,
            photo_folder_id VARCHAR (100) NOT NULL,
            photo_full_name VARCHAR)
            """
        )

    def add_violation(self, *, violation: dict):
        """Наполнение таблицы при первом запуске"""

        location = violation.get("location", None)
        if violation.get("year") == '2021' and violation.get("name") == 'Коршаков Алексей Сергеевич':
            location = 'ст. Аминьевская'

        work_shift = violation.get("work_shift", None)
        function = violation.get("function", None)
        name = violation.get("name", None)
        parent_id = violation.get("parent_id", None)
        violation_id = violation.get('violation_id', None)
        user_id = violation.get('user_id', None)
        user_fullname = violation.get('user_fullname', None)
        report_folder_id = violation.get('report_folder_id', None)
        file_id = violation.get('file_id', None)
        data = violation.get('data', None)
        day = violation.get('day', None)
        month = violation.get('month', None)
        year = violation.get('year', None)
        now = violation.get('now', None)
        main_category = violation.get('main_category', None)
        general_contractor = violation.get('general_contractor', None)
        category = violation.get('category', None)
        comment = violation.get('comment', None)
        act_required = violation.get('act_required', None)
        description = violation.get('description', None)
        elimination_time = violation.get('elimination_time', None)
        incident_level = violation.get('incident_level', None)
        violation_category = violation.get('violation_category', None)
        coordinates = violation.get('coordinates', None)
        latitude = violation.get('latitude  DEFAULT', None)
        longitude = violation.get('longitude  DEFAULT', None)
        json_folder_id = violation.get('json_folder_id', None)
        json_file_path = violation.get('json_file_path', None)
        json_full_name = violation.get('json_full_name', None)
        photo_file_path = violation.get('photo_file_path', None)
        photo_folder_id = violation.get('photo_folder_id', None)
        photo_full_name = violation.get('photo_full_name', None)

        with self.connection:
            return self.cursor.execute(
                "INSERT INTO `violations` (`location`,`work_shift` ,`function` ,`name` ,`parent_id`,"
                "`violation_id`, `user_id`, `user_fullname`, `report_folder_id`, `file_id`,"
                " `data`,`day`,`month`, `year`, `now`,"
                "`main_category`,`general_contractor`,`category`,`comment`,`act_required`,"
                "`description`,`elimination_time`,`incident_level`,`violation_category`, `coordinates`,"
                "`latitude`,`longitude`,`json_folder_id`,`json_file_path`,`json_full_name`,"
                "`photo_file_path`,`photo_folder_id`,`photo_full_name`)"
                "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    location, work_shift, function, name, parent_id,
                    violation_id, user_id, user_fullname, report_folder_id, file_id,
                    data, day, month, year, now,
                    main_category, general_contractor, category, comment, act_required,
                    description, elimination_time, incident_level, violation_category, coordinates,
                    latitude, longitude, json_folder_id, json_file_path, json_full_name,
                    photo_file_path, photo_folder_id, photo_full_name
                )
            )

    def violation_exists(self, file_id: int):
        """Проверка наличия violation_id в базе"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `violations` WHERE `file_id` = ?',
                                         (file_id,)).fetchall()
            return bool(len(result))

    def delete_violation(self, file_id: int):
        #  Удаление записи
        with self.connection:
            return self.cursor.execute("DELETE FROM `violations` WHERE `file_id` = ?", (file_id,))

    def get_info_violations(self, file_id: int):
        # получение информации по юзеру
        with self.connection:
            return self.cursor.execute("SELECT * FROM `violations` WHERE `file_id` = ?",
                                       (file_id,)).fetchone()

    def count_violations(self):
        # вывод кол-ва юзеров
        with self.connection:
            return self.cursor.execute('SELECT COUNT(*) FROM `violations`').fetchone()

    def all_violations(self):
        # вывод кол-ва юзеров+
        with self.connection:
            return self.cursor.execute('SELECT * FROM `violations`').fetchall()

    # def add_violation(self, username: str, user_id: int, language_code, is_bot):
    #     #  Добавляем нового юзера
    #     with self.connection:
    #         return self.cursor.execute(
    #             "INSERT INTO `violations` (`username`, `user_id`, `language_code`, `is_bot`) VALUES(?,?,?,?)",
    #             (username, user_id, language_code, is_bot))
    #
    # def set_nickname(self, user_id: int, nickname: str):
    #     with self.connection:
    #         return self.cursor.execute('UPDATE `violations` SET `nickname` = ? WHERE `user_id` = ?',
    #                                    (nickname, user_id,))
    #
    # def set_signup(self, user_id: int, signup):
    #     with self.connection:
    #         return self.cursor.execute('UPDATE `violations` SET `signup` = ? WHERE `user_id` = ?', (signup, user_id,))
    #
    # def set_time_sup(self, user_id: int, time_sub):
    #     with self.connection:
    #         current_time_sup = self.get_time_sup(user_id)
    #         if current_time_sup:
    #             sum_time_sup = current_time_sup + time_sub - time.time()
    #         else:
    #             sum_time_sup = time_sub
    #         return self.cursor.execute('UPDATE `violations` SET `time_sub` = ? WHERE `user_id` = ?',
    #                                    (sum_time_sup, user_id,))
    #
    # def get_time_sup(self, user_id: int) -> int:
    #     # поиск времени юзера
    #     time_sup = 0
    #     with self.connection:
    #         result = self.cursor.execute('SELECT `time_sub` FROM `violations` WHERE `user_id` = ?',
    #                                      (user_id,)).fetchall()
    #         for row in result:
    #             time_sup = int(row[0])
    #         return time_sup if time_sup else 0
    #
    # def get_signup(self, user_id: int):
    #
    #     with self.connection:
    #         signup = ""
    #         result = self.cursor.execute('SELECT `signup` FROM `violations` WHERE `user_id` = ?',
    #         (user_id,)).fetchall()
    #         for row in result:
    #             signup = str(row[0])
    #         return signup
    #
    # def get_nickname(self, user_id: int) -> str:
    #     """Поиск имени изера """
    #     with self.connection:
    #         result = self.cursor.execute("SELECT `nickname` FROM `violations` WHERE `user_id` = ?",
    #                                      (user_id,)).fetchall()
    #         for row in result:
    #             nickname = str(row[0])
    #         return nickname
    #
    # def get_sub_status(self, user_id: int) -> bool:
    #     """Поиск подписки изера"""
    #     with self.connection:
    #         result = self.cursor.execute("SELECT `time_sub` FROM `violations` WHERE `user_id` = ?",
    #                                      (user_id,)).fetchall()
    #         for row in result:
    #             time_sub = int(row[0])
    #
    #         if time_sub > int(time.time()):
    #             return True
    #         else:
    #             return False


db_file: str = WORK_PATH + '\\HSEViolationsDataBase.db'  # type: ignore
DataBase(db_file=db_file).create_table()
violation_file: str = 'C:/Users/KDeusEx/PycharmProjects/HSE_Bot/user_data/373084462/data_file/01.10.2021/json/' \
                      'report_data___01.10.2021___373084462___9437.json'


async def run_init():
    violation = await read_json_file(file=violation_file)

    if not violation:
        print('ERROR')
        exit(1)

    DataBase(db_file=db_file).add_violation(
        violation=violation)


async def write_json(violation):
    """Запись в файл"""
    if not os.path.isfile(violation['json_full_name']):
        print(f"FileNotFoundError {violation['json_full_name']} ")

        date_violation = violation['file_id'].split('___')[0]

        violation['json_full_name'] = \
            f"C:\\Users\\KDeusEx\\PycharmProjects\\HSE_Bot\\user_data\\373084462\\data_file" \
            f"\\{date_violation}\\json\\report_data___{violation['file_id']}.json"
        violation['photo_full_name'] = \
            f"C:\\Users\\KDeusEx\\PycharmProjects\\HSE_Bot\\user_data\\373084462\\data_file" \
            f"\\{date_violation}\\photo\\report_data___{violation['file_id']}.jpg"

        await write_json_file(data=violation, name=violation['json_full_name'])
        return

    await write_json_file(data=violation, name=violation['json_full_name'])


async def run():
    user_chat_id = '373084462'
    params: dict = {
        'all_files': True,
        'file_path': f"C:/Users/KDeusEx/PycharmProjects/HSE_Bot/user_data/{user_chat_id}/data_file",
        'user_file': f"C:/Users/KDeusEx/PycharmProjects/HSE_Bot/user_data/{user_chat_id}/{user_chat_id}.json"
    }

    if not os.path.exists(params['file_path']):
        print(f"ERROR file: {params['file_path']} don't exists")
        exit(0)

    if not os.path.exists(params['user_file']):
        print(f"ERROR file: {params['user_file']} don't exists")
        exit(0)

    if not os.path.isfile(params['user_file']):
        print(f"ERROR file: {params['user_file']} not a file")
        exit(0)

    json_file_list = await get_files(params['file_path'], endswith=".json")

    error_counter: int = 0
    comment_counter: int = 0
    act_required_counter: int = 0
    elimination_time_counter: int = 0
    general_contractor_counter: int = 0
    incident_level_counter: int = 0

    for counter, violation_file in enumerate(json_file_list, start=1):

        violation = await read_json_file(file=violation_file)
        user_data_json_file = await read_json_file(file=params['user_file'])

        if not violation.get("location"):
            violation["location"] = user_data_json_file.get("name_location")
            await write_json(violation=violation)

        if not violation.get("work_shift"):
            violation["work_shift"] = user_data_json_file.get("work_shift")
            await write_json(violation=violation)

        if not violation.get("function"):
            violation["function"] = user_data_json_file.get("function")
            await write_json(violation=violation)

        if not violation.get("name"):
            violation["name"] = user_data_json_file.get("name")
            await write_json(violation=violation)

        if not violation.get("parent_id"):
            violation["parent_id"] = user_data_json_file.get("parent_id")
            await write_json(violation=violation)

        file_id = violation.get('file_id')

        if not violation.get('general_contractor'):
            print(f"ERROR file: {file_id} don't get 'general_contractor' parameter")
            error_counter += 1
            general_contractor_counter += 1

            os.remove(violation_file)
            print(f"file: {violation_file} is remove")
            continue

        if not violation.get('elimination_time'):
            print(f"ERROR file: {file_id} don't get 'elimination_time' parameter")
            error_counter += 1
            elimination_time_counter += 1
            violation['elimination_time'] = '1 день'
            await write_json(violation=violation)
            continue

        if not violation.get('incident_level'):
            print(f"ERROR file: {file_id} don't get 'incident_level' parameter")
            error_counter += 1
            incident_level_counter += 1
            violation['incident_level'] = 'Без последствий'
            await write_json(violation=violation)
            continue

        if not violation.get('act_required'):
            print(f"ERROR file: {file_id} don't get 'act_required' parameter")
            error_counter += 1
            act_required_counter += 1
            os.remove(violation_file)
            print(f"file: {violation_file} is remove")
            continue

        if not violation.get('comment'):
            print(f"ERROR file: {file_id} don't get 'comment' parameter")
            error_counter += 1
            comment_counter += 1
            continue

        if not DataBase(db_file=db_file).violation_exists(file_id):
            DataBase(db_file=db_file).add_violation(violation=violation)
            print(f"{counter} file {violation.get('file_id')} add in db {db_file}")

    print(f"errors {error_counter} in {len(json_file_list)} items")
    print(f"general_contractor_counter {general_contractor_counter} in {error_counter} items")
    print(f"elimination_time_counter {elimination_time_counter} in {error_counter} items")
    print(f"act_required_counter {act_required_counter} in {error_counter} items")
    print(f"incident_level_counter {incident_level_counter} in {error_counter} items")
    print(f"comment_counter {comment_counter} in {error_counter} items")


if __name__ == '__main__':
    asyncio.run(run())

    print(f'count_violations {DataBase(db_file=db_file).count_violations()}')

# if __name__ == '__main__':
#
#     db = DataBase('database.db')
#     end__ = True
#
#     while end__:
#         all_user = db.all_user()
#         if not all_user:
#             break
#
#         for item in all_user:
#             print(f'ID {item[1]} subscription expiration {float(time.time()) > item[2]}')
#             if float(time.time()) > item[2] != 0:
#                 db.delete_profile(user_id=item[1])
#                 print(f"user_id {item[1]} has been removed due to channel subscription expiration")
#         print("i'm work")
#         time.sleep(5)
#
# class dbworker:
#     def __init__(self, database_file):+
#         self.connection = sqlite3.connect(database_file)
#         self.cursor = self.connection.cursor()
#
#     def violation_exists(self, user_id):
#         # Проверка есть ли юзер в бд
#         with self.connection:
#             result = self.cursor.execute('SELECT * FROM `users` WHERE `telegram_id` = ?', (user_id,)).fetchall()
#             return bool(len(result))
#
#     def add_user(self, telegram_username, telegram_id, full_name):
#         # Добавляем нового юзера
#         with self.connection:
#             return self.cursor.execute(
#                 "INSERT INTO `users` (`telegram_username`, `telegram_id`,`full_name`) VALUES(?,?,?)",
#                 (telegram_username, telegram_id, full_name))
#
#     def create_profile(self, telegram_id, telegram_username, name, description, city, photo, sex, age, social_link):
#         # Создаём анкету
#         with self.connection:
#             return self.cursor.execute(
#                 "INSERT INTO `profile_list`
#                 (`telegram_id`,`telegram_username`,`name`,`description`,`city`,`photo`,`sex`,`age`,`social_link`)
#                 VALUES(?,?,?,?,?,?,?,?,?)",
#                 (telegram_id, telegram_username, name, description, city, photo, sex, age, social_link))
#
#     def profile_exists(self, user_id):
#         # Проверка есть ли анкета в бд
#         with self.connection:
#             result = self.cursor.execute("SELECT * FROM `profile_list` WHERE
#             `telegram_id` = ?", (user_id,)).fetchall()
#             return bool(len(result))
#
#     def delete_profile(self, user_id):
#         # Удаление анкеты
#         with self.connection:
#             return self.cursor.execute("DELETE FROM `profile_list` WHERE `telegram_id` = ?", (user_id,))
#
#     def all_profile(self, user_id):
#         # поиск по анкетам
#         with self.connection:
#             return self.cursor.execute("SELECT * FROM `profile_list` WHERE `telegram_id` = ?", (user_id,)).fetchall()
#
#     def edit_description(self, description, user_id):
#         # изменение описания
#         with self.connection:
#             return self.cursor.execute('UPDATE `profile_list` SET `description` = ? WHERE `telegram_id` = ?',
#                                        (description, user_id))
#
#     def edit_age(self, age, user_id):
#         # изменение возвраста
#         with self.connection:
#             return self.cursor.execute('UPDATE `profile_list` SET `age` = ? WHERE `telegram_id` = ?', (age, user_id))
#
#     def search_profile(self, city, age, sex):
#         # поиск хаты
#         try:
#             if str(sex) == 'мужчина':
#                 sex_search = 'женщина'
#             else:
#                 sex_search = 'мужчина'
#             with self.connection:
#                 return self.cursor.execute(
#                     "SELECT `telegram_id` FROM `profile_list` WHERE `city` = ? AND `sex` = ? AND
#                     `age` BETWEEN ? and 54",
#                     (city, sex_search, age)).fetchall()
#         except Exception as e:
#             print(e)
#
#     def get_info(self, user_id):
#         # получение ифнормации по профилю
#         with self.connection:
#             return self.cursor.execute("SELECT * FROM `profile_list` WHERE `telegram_id` = ?", (user_id,)).fetchone()
#
#     def search_profile_status(self, user_id):
#         # возвращение статуса
#         with self.connection:
#             return self.cursor.execute("SELECT `search_id` FROM `users` WHERE
#             `telegram_id` = ?", (user_id,)).fetchone()
#
#     def edit_profile_status(self, user_id, num):
#         # изменение статуса
#         with self.connection:
#             return self.cursor.execute('UPDATE `users` SET `search_id` = ? WHERE
#             `telegram_id` = ?',
#                                        (str(num + 1), user_id))
#
#     def edit_zero_profile_status(self, user_id):
#         # изменение статуса на 0 когда анкеты заканчиваются
#         with self.connection:
#             return self.cursor.execute('UPDATE `users` SET `search_id` = 0 WHERE
#             `telegram_id` = ?', (user_id,))
#
#     def set_city_search(self, city, user_id):
#         # задования города для поиска
#         with self.connection:
#             return self.cursor.execute('UPDATE `users` SET `city_search` = ? WHERE
#             `telegram_id` = ?', (city, user_id))
#
#     def get_info_user(self, user_id):
#         # получение информации по юзеру
#         with self.connection:
#             return self.cursor.execute("SELECT * FROM `users` WHERE `telegram_id` = ?", (user_id,)).fetchone()
#
#     def check_rating(self, user_id):
#         # чек по рейтингу
#         with self.connection:
#             return self.cursor.execute("SELECT `rating` FROM `profile_list` WHERE `telegram_id` = ?",
#                                        (user_id,)).fetchone()
#
#     def up_rating(self, count, user_id):
#         # добавление по рейтингу
#         with self.connection:
#             return self.cursor.execute('UPDATE `profile_list` SET `rating` = ? WHERE `telegram_id` = ?',
#                                        (count + 1, user_id))
#
#     def top_rating(self):
#         # вывод топа по рейтингу
#         with self.connection:
#             return self.cursor.execute('SELECT `telegram_id` FROM `profile_list` ORDER BY
#             `rating` DESC LIMIT 5').fetchall()
