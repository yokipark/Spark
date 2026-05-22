# localization.py

LANGUAGES = {
    "RU": {
        # Global
        "export": "ЭКСПОРТ",
        "app_title_1": "Картотека",
        "app_title_2": "библиотекаря",
        "history": "История",
        "lib_info": "ИНФОРМАЦИЯ О БИБЛИОТЕКЕ",
        # sidebar
        "main": "🏠     Главное",
        "books": "📋     Книжный фонд",
        "readers": "👤     Читатель",
        "issue": "🕒     Выдача/Возврат",
        "reports": "📊     Отчеты",
        "settings": "⚙️     Настройки",
        # Переводы для Issue/Return Page (Добавленное)
        "reader_caps": "ЧИТАТЕЛИ",
        "book_caps": "КНИГА",
        "enter_fio_or_id": "Введите ФИО или ID...",
        "enter_book_id": "Введите ID книги...",
        "book_code_label": "Код книги",
        "reader_id_label": "ID Читателя",
        "history": "История",
        "books_on_hand_text": "книг(и) на руках",
        "user_books_title": "Книги в руках",
        "no_history": "Нет истории",
        "issue_btn": "ВЫДАЧА",
        "return_btn": "ВОЗВРАТ",
        "librarian": "Библиотекарь",
        "profile": "ПРОФИЛЬ",
        "Login": "ВОЙТИ",
        "reader":"Читатель",
        # login 
        "ID сотрудника": "ID сотрудника",
        "Пароль": "Пароль",
        "incorrect_password": "Неверный ID или пароль!",

        # dashboard
        "books_on_loan": "Книг на руках",
        "overdue": "Просрочено",
        "new_readers": "Новые читатели",
        "weekly_activity": "Активность за неделю",
        "quick_issue": "Быстрая выдача",
        "accept_return": "Принять возврат",
        "add_reader": "Добавить читателя",
        "recent_actions": "Последние действия",
        "search_placeholder": "Поиск по всей базе...",
        "reader_name": "ФИО читателя",
        "quick": "Быстрые",
        "actions": "Действия",
        "time": "Время",

        # bookfund 
        "Поиск по названию, автору или №...": "Поиск по названию, автору или №...",
        "add_book": "ДОБАВИТЬ КНИГУ",
        "cancel": "Отмена",
        
        # table & badges
        "inv_num": "Инвентарный №",
        "book_title": "Название книги",
        "author": "Автор",
        "genre": "Жанр",
        "status": "Статус", 
        "place": "Место",
        "in_stock": "В наличии",
        "borrowed": "Выдана",
        
        # settings 
        "change_pass": "Сменить пароль",
        "system": "СИСТЕМА",
        "print": "Печать",
        "sound": "Звук",
        "notifications": "Уведомления",
        "interface": "ИНТЕРФЕЙС",
        "user": "ПОЛЬЗОВАТЕЛЬ",
        "dark_mode": "Темная тема",
        "lang": "Язык / Language",
        
        # messages
        "exp_success_title": "Экспорт завершен",
        "exp_success_msg": "Данные успешно выгружены в файл:\n{}\n\nИщите файл в папке 'exports/'",
        "exp_error_title": "Ошибка экспорта",
        "exp_error_msg": "Не удалось выполнить экспорт:\n{}",
        "app_title_1": "Картотека",
        "app_title_2": "библиотекаря",
        "in_stock": "В наличии",
        "borrowed": "Выдана",
        "total_issued": "ВСЕГО ВЫДАНО",
        "new_books": "НОВЫХ КНИГ",
        "new_readers_caps": "НОВЫХ ЧИТАТЕЛЕЙ",
        "popular_genres": "ПОПУЛЯРНЫЕ ЖАНРЫ",
        "active_readers_caps": "АКТИВНЫЕ ЧИТАТЕЛИ",
        "active_label": "Активные\nчитатели",
        "dropped_label": "Бросили\n",
        "exp_success_title": "Экспорт завершен",
        "exp_success_msg": "Данные успешно выгружены в файл:\n{}\n\nИщите файл в папке 'exports/'",
        "exp_error_title": "Ошибка экспорта",
        "exp_error_msg": "Не удалось выполнить экспорт:\n{}",
        "enter_fio_or_id": "Введите ФИО или ID читателя",
        "user_name": "Имя пользователя",
        "readersx":"ЧИТАТЕЛИ",
    },
    "KG": {
        # Global
        "export": "ЭКСПОРТТОО",
        "app_title_1": "Картотека",
        "app_title_2": "китепканачы",
        "history":"История",
        # sidebar
        "main": "🏠 Башкы бет",
        "books": "📋 Китеп фонду",
        "readers": "👤 Окурман",
        "issue": "🕒 Берүү/Кайтаруу",
        "reports": "📊 Отчеттор",
        "settings": "⚙️ Жөндөөлөр",
        "readers":"ОКУРМАНДАР",
        "librarian": "Китепканачы",
        "profile": "ПРОФИЛЬ",
        "reader_caps": "ОКУРМАНДАР",
        "book_caps": "КИTЕП",
        "enter_fio_or_id": "Аты-жөнүн же IDсин жазыңыз...",
        "enter_book_id": "Китептин IDсин жазыңыз...",
        "book_code_label": "Китептин коду",
        "reader_id_label": "Окурмандын IDси",
        "history": "Тарыхы",
        "books_on_hand_text": "китеп колунда бар",
        "user_books_title": "Колундагы китептер",
        "no_history": "Тарыхы бош",
        "issue_btn": "БЕРҮҮ",
        "return_btn": "КАЙТАРУУ",
        # login
        "ID сотрудника": "Ишкердин IDси",
        "Пароль": "Пароль",
        "Login": "КИРҮҮ",
        "incorrect_password": "ID же пароль туура эмес!",
        
        # dashboard
        "books_on_loan": "Колдонуудагы китептер",
        "overdue": "Мөөнөтү өткөн",
        "new_readers": "Жаңы окурмандар",
        "weekly_activity": "Аптадагы активдүүлүк",
        "quick_issue": "Тез берүү",
        "accept_return": "Кайтарууну кабыл алуу",
        "add_reader": "Окурман кошуу",
        "recent_actions": "Акыркы аракеттер",
        "search_placeholder": "База боюнча издөө...",
        "reader_name": "Окурмандын аты-жөнү",
        "quick": "Тез",
        "actions": "Аракет",
        "time": "Убакыт",
        "reader":"Окурман",
        "readersx":"Окурмандар",
        # bookfund 
        "Поиск по названию, автору или №...": "Аталышы, автору же № боюнча издөө...",
        "add_book": "КИТЕП КОШУУ",
        "cancel": "Чыгуу",

        # table & badges
        "inv_num": "Инвертардык №",
        "book_title": "Китептин аталышы",
        "author": "Автору",
        "genre": "Жанры",
        "status": "Статусу", 
        "place": "Орду",
        "in_stock": "Кабыл алынды",
        "borrowed": "Берүү",

        # settings 
        "change_pass": "Сырсөздү өзгөртүү",
        "system": "СИСТЕМА",
        "print": "Басып чыгаруу",
        "sound": "Үн",
        "notifications": "Билдирүүлөр",
        "interface": "ИНТЕРФЕЙС",
        "user": "КОЛДОНУУЧУ",
        "dark_mode": "Караңгы тема",
        "lang": "Тил / Language",
        
        # messages
        "exp_success_title": "Экспорт аяктады",
        "exp_success_msg": "Маалыматтар файлга ийгиликтүү жүктөлдү:\n{}\n\nФайлды 'exports/' папкасынан издеңиз",
        "exp_error_title": "Экспорт катасы",
        "exp_error_msg": "Экспорттоо аткарылган жок:\n{}",
        "app_title_1": "Картотека",
        "app_title_2": "китепканачы",
        "in_stock": "Кабыл алынды",
        "borrowed": "Берүү",
        "total_issued": "БАРДЫГЫ БЕРИЛДИ",
        "new_books": "ЖАҢЫ КИТЕПТЕР",
        "new_readers_caps": "ЖАҢЫ ОКУРМАНДАР",
        "popular_genres": "ПОПУЛЯРДУУ ЖАНРЛАР",
        "active_readers_caps": "АКТИВДҮҮ ОКУРМАНДАР",
        "active_label": "Активдүү\nокурмандар",
        "dropped_label": "Таштап кетти\n",
        "exp_success_title": "Экспорт аяктады",
        "exp_success_msg": "Маалыматтар файлга ийгиликтүү жүктөлдү:\n{}\n\nФайлды 'exports/' папкасынан издеңиз",
        "exp_error_title": "Экспорт катасы",
        "exp_error_msg": "Экспорттоо аткарылган жок:\n{}",
        "enter_fio_or_id": "окурмандын аты-жөнүн же IDсин жазыныз",
    
    },
    "EN": {
        # Global
        "export": "EXPORT",
        "app_title_1": "Card Index",
        "app_title_2": "Librarian",
        "history": "History",
        # sidebar
        "main": "🏠 Dashboard",
        "books": "📋 Book Fund",
        "readers": "👤 Readers",
        "issue": "🕒 Issue/Return",
        "reports": "📊 Reports",
        "settings": "⚙️ Settings",
        "reader":"Reader",
        "librarian": "Librarian",
        "profile": "PROFILE",
        "readersx":"READERS",
        "reader": "Reader",
        # login
        "ID сотрудника": "Worker ID",
        "Пароль": "Password",
        "Login": "LOGIN",
        "incorrect_password": "Incorrect ID or password!",
        # Переводы для Issue/Return Page (Добавленное)
        "reader_caps": "READERS",
        "book_caps": "BOOK",
        "enter_fio_or_id": "Enter name or ID...",
        "enter_book_id": "Enter book ID...",
        "book_code_label": "Book Code",
        "reader_id_label": "Reader ID",
        "history": "History",
        "books_on_hand_text": "books on hand",
        "user_books_title": "Books on hand",
        "no_history": "No history",
        "issue_btn": "ISSUE",
        "return_btn": "RETURN",
        # dashboard 
        "books_on_loan": "Books on loan",
        "overdue": "Overdue",
        "new_readers": "New readers",
        "weekly_activity": "Weekly activity",
        "quick_issue": "Quick issue",
        "accept_return": "Accept return",
        "add_reader": "Add reader",
        "recent_actions": "Recent actions",
        "search_placeholder": "Search database...",
        "reader_name": "Reader name",
        "quick": "Quick",
        "actions": "Action",
        "time": "Time",
        
        # bookfund 
        "Поиск по названию, автору или №...": "Search by name, author or №...",
        "add_book": "ADD BOOK",
        "cancel": "Cancel",
        
        # table & badges
        "inv_num": "Inventory №",
        "book_title": "Book Title",
        "author": "Author",
        "genre": "Genre",
        "status": "Status",
        "place": "Place",
        "in_stock": "In Stock",
        "borrowed": "Borrowed",

        # settings 
        "change_pass": "Change Password",
        "system": "SYSTEM",
        "print": "Print",
        "sound": "Sound",
        "notifications": "Notifications",
        "interface": "INTERFACE",
        "user": "USER",
        "dark_mode": "Dark Mode",
        "lang": "Language",
        
        # messages
        "exp_success_title": "Export Completed",
        "exp_success_msg": "Data successfully exported to file:\n{}\n\nLook for the file in 'exports/' folder",
        "exp_error_title": "Export Error",
        "exp_error_msg": "Failed to complete export:\n{}",
        "app_title_1": "Card Index",
        "app_title_2": "Librarian",
        "in_stock": "In Stock",
        "borrowed": "Borrowed",
        "total_issued": "TOTAL ISSUED",
        "new_books": "NEW BOOKS",
        "new_readers_caps": "NEW READERS",
        "popular_genres": "POPULAR GENRES",
        "active_readers_caps": "ACTIVE READERS",
        "active_label": "Active\nreaders",
        "dropped_label": "Dropped\n",
        "exp_success_title": "Export Completed",
        "exp_success_msg": "Data successfully exported to file:\n{}\n\nLook for the file in 'exports/' folder",
        "exp_error_title": "Export Error",
        "exp_error_msg": "Failed to complete export:\n{}",
        "enter_fio_or_id": "Enter user name or ID",
    }
}

current_lang = "RU"

def set_lang(lang_code):
    global current_lang
    if lang_code in LANGUAGES:
        current_lang = lang_code

def get(key, default_value=None):
    """Возвращает перевод по ключу. Если ключа нет, возвращает default_value или сам key."""
    # Если default_value не передан, используем сам key в качестве резервного текста
    if default_value is None:
        default_value = key
        
    return LANGUAGES[current_lang].get(key, default_value)
