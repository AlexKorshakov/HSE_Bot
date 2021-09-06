class Messages:
    write_to_developer: str = f'Чтобы написать разработчику нажмите /developer'
    help_message: str = f"Справка по командам бота /help \n" \
                        f'для начала работы и регистрации в системе (повторной регистрации) нажмите /start \n' \
                        f'{write_to_developer}'
    wait: str = f"Это может занять нескоторое время"
    report_done: str = f"Отчет сформирован"
    report_start: str = f"Начинаю генерацию отчета"
    cancel: str = f"Отмена!"
    register_canceled: str = f"OK! если хотите зарегистрироваться, отправьте /start заново"
    hi: str = f"Привет"
    user_greeting: str = f'Этот бот предназначен для регистрации нарушений и создания ежедневных отчетов \n' \
                         f'Для начала работы просто отправьте фото боту'
    ask_name: str = f"Введите ваше ФИО полностью"
    ask_function: str = f"Введите вашу должность полностью"
    ask_phone_number: str = f"Отправь мне свой номер телефона с кодом (пример +7xxxxxxxxxx)"
    ask_location: str = f"Введите с момощью клавиатуру ваще местоположение (пример Аминьевское шоссе)"
    invalid_input: str = f"Неправильный ввод данных! \n" \
                         f"Отправь номер телефона в формате (без пробелов)(пример +7xxxxxxxxxx)"
    registration_completed_successfully: str = "регистрация прошла успешно"
    registration_begin: str = f"Начинаю процедуру регистрации"
    workbook_not_found: str = f"Файл с отчетом не найден! Обратитесь к разработчику! \n" \
                              f'чтобы написать разработчику нажмите /developer'
    worksheet_not_found: str = f"Страница с отчетом не найден! Обратитесь к разработчику! \n" \
                               f'чтобы написать разработчику нажмите /developer'
    fill_report_path_not_found: str = f"Путь к файлу с отчетом не найден! Обратитесь к разработчику! \n" \
                                      f'чтобы_написать_разработчику_нажмите_/developer'
    dataframe_not_found: str = f'Массив данных не найден! Обратитесь к разработчику! \n' \
                               f'чтобы написать разработчику нажмите /developer'
    file_list_not_found: str = f"Список файлов не найден! \n" \
                               f'попытка загрузить данные с сервера'
    workbook_not_create: str = f"Файл с отчетом не создан! Обратитесь к разработчику! \n" \
                               f'чтобы написать разработчику нажмите /developer'
    err_authorized_google_drive: str = f"Не удалось авторизоваться на Google Drive!"
    report_begin: str = f"Запись загружается"
    report_completed_successfully: str = f"Запись загружена"
    bot_start: str = f"Бот успешно запущен..."
