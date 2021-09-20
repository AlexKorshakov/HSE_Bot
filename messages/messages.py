class Messages:
    """Класс со всеми текстовыми сообщенияим
    """
    write_to_developer: str = f'Чтобы написать разработчику нажмите /developer'
    help_message: str = f"Справка по командам бота /help \n" \
                        f'для начала работы и регистрации в системе (повторной регистрации) нажмите /start \n' \
                        f'{write_to_developer}'
    wait: str = f"Это может занять нескоторое время"

    report_done: str = f"Отчет сформирован на сервере"
    report_start: str = f"Начинаю генерацию отчета"
    report_sent_successfully: str = f"Отчет успешно отправлен"
    report_begin: str = f"Запись загружается"
    report_completed_successfully: str = f"Запись загружена"

    cancel: str = f"Отмена!"
    register_canceled: str = f"OK! если хотите зарегистрироваться, отправьте /start заново"
    hi: str = f"Привет"
    user_greeting: str = f'Этот бот предназначен для регистрации нарушений и создания ежедневных отчетов \n' \
                         f'Для начала работы просто отправьте фото боту'
    ask_name: str = f"Введите ваше ФИО полностью"
    ask_function: str = f"Введите вашу должность полностью"
    ask_phone_number: str = f"Отправь мне свой номер телефона с кодом (пример +7xxxxxxxxxx)"
    ask_work_shift: str = f"В какую смену вы работаете? (пример дневная смена / ночная смена)"
    ask_location: str = f"Введите с момощью клавиатуры ваще местоположение (пример Аминьевское шоссе)"
    invalid_input: str = f"Неправильный ввод данных! \n" \
                         f"Отправь номер телефона в формате (без пробелов)(пример +7xxxxxxxxxx)"

    begin_registration: str = f"Начинаю процедуру регистрации"
    begin_registration_report: str = f"Начинаю процедуру регистрации отчета"

    error_workbook_not_found: str = f"Файл с отчетом не найден! Обратитесь к разработчику! \n" \
                                    f'чтобы написать разработчику нажмите /developer'
    error_worksheet_not_found: str = f"Страница с отчетом не найден! Обратитесь к разработчику! \n" \
                                     f'чтобы написать разработчику нажмите /developer'
    error_fill_report_path_not_found: str = f"Путь к файлу с отчетом не найден! Обратитесь к разработчику! \n" \
                                            f'чтобы написать разработчику нажмите /developer'
    error_dataframe_not_found: str = f'Не удалось получить массив данных для формирования отчета! \n' \
                                     'Обратитесь к разработчику! \n' \
                                     f'чтобы написать разработчику нажмите /developer'
    error_file_list_not_found: str = f"Список файлов не найден! \n" \
                                     f'попытка загрузить данные с сервера'
    error_workbook_not_create: str = f"Файл с отчетом не создан! Обратитесь к разработчику! \n" \
                                     f'чтобы написать разработчику нажмите /developer'

    error_registration_file_list_not_found: str = "Не удалось получить регистрационные данные!" \
                                                  " Обратитесь к разработчику! \n" \
                                                  f'чтобы написать разработчику нажмите /developer'
    error_authorized_google_drive: str = f"Не удалось авторизоваться на Google Drive!"
    error_upload_on_web: str = "файл не обнаружен, загрузка на web прервана"

    error_location_name_not_found: str = "Не найдены данные о местоположении!"

    successfully_bot_start: str = f"Бот успешно запущен..."
    successfully_save_data_on_g_drive: str = "Данные сохранены в Google Drive"
    successfully_registration_completed: str = "регистрация прошла успешно"
