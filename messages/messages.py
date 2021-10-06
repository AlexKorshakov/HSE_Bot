class Messages:
    """Класс со всеми текстовыми сообщенияим
    """
    url_registration_violation: str = f"https://www.youtube.com/channel/UCbq0Z7aDzYc3S4dAPTFDtkA"

    write_to_developer: str = f'Чтобы написать разработчику нажмите /developer'
    help_message: str = f"Справка по командам бота /help \n" \
                        f'\n' \
                        f"Видео инструкция {url_registration_violation}" \
                        f'\n' \
                        f'Для регистрации в системе (повторной регистрации) нажмите /start \n' \
                        f'{write_to_developer}'
    wait: str = f"Это может занять нескоторое время"
    cancel: str = f"Отмена!"
    hi: str = f"Привет"
    user_greeting: str = f'Этот бот предназначен для регистрации нарушений и создания ежедневных отчетов \n' \
                         f'Для начала работы просто отправьте фото боту'

    bot_setting_commands: str = 'Установка комманд бота...'

    class Registration:
        user_registration: str = f"Начинаю процедуру регистрации"
        # start_registration: str = f"Начинаю процедуру регистрации отчета"
        confirm: str = f"При завершении регистрации дальнейшее изменение невозможно!"
        canceled: str = f"OK! если хотите зарегистрироваться, отправьте /start заново"
        cancel: str = f"Отмена!"

    class Removed:
        violation_data_pc: str = "Запись о нарушении удалена с сервера"
        violation_photo_pc: str = "Фотоматериалы нарушения удалены с сервера"
        violation_data_gdrive: str = "Запись о нарушении удалена с Google Drive"
        violation_photo_gdrive: str = "Фотоматериалы нарушения удалены с Google Drive"

    class Ask:
        name: str = f"Введите ваше ФИО полностью"
        function: str = f"Введите вашу должность полностью"
        phone_number: str = f"Отправь мне свой номер телефона с кодом (пример +7xxxxxxxxxx)"
        work_shift: str = f"В какую смену вы работаете? (пример дневная смена / ночная смена)"
        location: str = f"Введите с момощью клавиатуры ваще местоположение (пример Аминьевское шоссе)"

    class Report:
        done: str = f"Отчет сформирован на сервере"
        start: str = f"Начинаю генерацию отчетов"
        sent_successfully: str = f"Отчет успешно отправлен"
        begin: str = f"Запись загружается"
        completed_successfully: str = f"Запись загружена"

    class Successfully:
        bot_start: str = f"Бот успешно запущен..."
        save_data_on_g_drive: str = "Данные сохранены в Google Drive"
        registration_completed: str = "Регистрация прошла успешно"
        registration_data_received: str = "Регистрационные данные получены"
        list_tutors_received: str = "Список поучателей получен"
        mail_send: str = "Письмо с отчетами успешно отправлено"
        letter_formed: str = "Письмо сформировано"

    class Enter:
        comment: str = "Введите комментарий"
        description_violation: str = "Введите описание нарушения"

    class Choose:
        answer: str = f"Выберите ответ"
        entry: str = f"Выберите запись по id"

    class Error:
        workbook_not_found: str = f"Файл с отчетом не найден! Обратитесь к разработчику! \n" \
                                  f'чтобы написать разработчику нажмите /developer'
        worksheet_not_found: str = f"Страница с отчетом не найден! Обратитесь к разработчику! \n" \
                                   f'чтобы написать разработчику нажмите /developer'
        fill_report_path_not_found: str = f"Путь к файлу с отчетом не найден! Обратитесь к разработчику! \n" \
                                          f'чтобы написать разработчику нажмите /developer'
        dataframe_not_found: str = f'Не удалось получить массив данных для формирования отчета! \n' \
                                   'Обратитесь к разработчику! \n' \
                                   f'чтобы написать разработчику нажмите /developer'
        file_list_not_found: str = f"Список файлов не найден! \n"  # \
        # f'попытка загрузить данные с сервера'
        workbook_not_create: str = f"Файл с отчетом не создан! Обратитесь к разработчику! \n" \
                                   f'чтобы написать разработчику нажмите /developer'

        registration_file_list_not_found: str = "Не удалось получить регистрационные данные!" \
                                                " Обратитесь к разработчику! \n" \
                                                f'чтобы написать разработчику нажмите /developer'
        authorized_google_drive: str = f"Не удалось авторизоваться на Google Drive!"
        upload_on_web: str = "Файл не обнаружен, загрузка на web прервана"
        file_not_found: str = "Файлы не найдены. Вероятно они были удалёны"
        location_name_not_found: str = "Не найдены данные о местоположении!"
        invalid_input: str = f"Отправь мне свой номер телефона с кодом (пример +7xxxxxxxxxx)"
        no_file_too_send: str = "Нет файлов для отправки"
