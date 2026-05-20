# localization.py

LANGUAGES = {
    "RU": {

        # Global

        "export": "ЭКСПОРТ",
        # sidebar
        "main": "🏠 Главное",
        "books": "📋 Книжный фонд",
        "readers": "👤 Читатель",
        "issue": "🕒 Выдача/Возврат",
        "reports": "📊 Отчеты",
        "settings": "⚙️ Настройки",


        "librarian": "Библиотекарь",
        "profile": "ПРОФИЛЬ",
        "Login": "ВОЙТИ",

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
                #table 

        "inv_num": "Инвертарный №",
        "book_title": "Название книги",
        "author": "Автор",
        "genre": "Жанр",
        "status": "Статус", 
        "place": "Место",
        
        # settings 
        "change_pass": "Сменить пароль",
        "system": "СИСТЕМА",
        "print": "Печать",
        "sound": "Звук",
        "notifications": "Уведомления",
        "interface": "ИНТЕРФЕЙС",
        "user": "ПОЛЬЗОВАТЕЛЬ",
        "dark_mode": "Темная тема",
        "lang": "Язык / Language"
    },
    "KG": {

        # Global

        "export": "ЭКСПОРТТОО",
        # sideabr
        "main": "🏠 Башкы бет",
        "books": "📋 Китеп фонду",
        "readers": "👤 Окурман",
        "issue": "🕒 Берүү/Кайтаруу",
        "reports": "📊 Отчеттор",
        "settings": "⚙️ Жөндөөлөр",


        "librarian": "Китепканачы",
        "profile": "ПРОФИЛЬ",

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
        # bookfund 

        "Поиск по названию, автору или №...": "Аталышы, автору же № боюнча издөө...",
        "add_book": "КИТЕП КОШУУ",
        "cancel": "Чыгуу",

                # table
        
        "inv_num": "Инвертардык №",
        "book_title": "Китептин аталышы",
        "author": "Автору",
        "genre": "Жанры",
        "status": "Статусу", 
        "place": "Орду",

        # settings 
        "change_pass": "Сырсөздү өзгөртүү",
        "system": "СИСТЕМА",
        "print": "Басып чыгаруу",
        "sound": "Үн",
        "notifications": "Билдирүүлөр",
        "interface": "ИНТЕРФЕЙС",
        "user": "КОЛДОНУУЧУ",
        "dark_mode": "Караңгы тема",
        "lang": "Тил / Language"
    },
    "EN": {
        # Global

        "export": "EXPORT",

        # sidebar
        "main": "🏠 Dashboard",
        "books": "📋 Book Fund",
        "readers": "👤 Readers",
        "issue": "🕒 Issue/Return",
        "reports": "📊 Reports",
        "settings": "⚙️ Settings",


        "librarian": "Librarian",
        "profile": "PROFILE",

        # login

        "ID сотрудника": "Worker ID",
        "Пароль": "Password",
        "Login": "LOGIN",
        "incorrect_password": "Incorrect ID or password!",

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
                # table 

        
        "inv_num": "Inventory №",
        "book_title": "Book Title",
        "author": "Author",
        "genre": "Genre",
        "status": "Status",
        "place": "Place",


        # settings 
        "change_pass": "Change Password",
        "system": "SYSTEM",
        "print": "Print",
        "sound": "Sound",
        "notifications": "Notifications",
        "interface": "INTERFACE",
        "user": "USER",
        "dark_mode": "Dark Mode",
        "lang": "Language"
    }
}

# По умолчанию ставим русский
current_lang = "RU"

def set_lang(lang_code):
    global current_lang
    if lang_code in LANGUAGES:
        current_lang = lang_code

def get(key):
    """Возвращает перевод по ключу."""
    return LANGUAGES[current_lang].get(key, key)
