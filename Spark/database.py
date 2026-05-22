import sqlite3
from datetime import datetime

DB_NAME = "library.db"

# --- Словарь для перевода месяцев ---
RU_MONTHS = {
    "01": "Январь", "02": "Февраль", "03": "Март", "04": "Апрель",
    "05": "Май", "06": "Июнь", "07": "Июль", "08": "Август",
    "09": "Сентябрь", "10": "Октябрь", "11": "Ноябрь", "12": "Декабрь"
}
RU_MONTHS_REV = {v: k for k, v in RU_MONTHS.items()}

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. Readers Table (ОБНОВЛЕННАЯ СХЕМА С НОВЫМИ КОЛОНКАМИ)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS readers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            inv_card TEXT UNIQUE,
            full_name TEXT NOT NULL,
            reg_date TEXT,
            books_current INTEGER DEFAULT 0,
            books_read INTEGER DEFAULT 0
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            inv_number TEXT NOT NULL UNIQUE,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            genre TEXT NOT NULL,
            status TEXT DEFAULT 'В наличии',
            place TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('admin', '1234')")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            inv_number TEXT,
            book_title TEXT,
            reader_name TEXT,
            action_type TEXT,
            timestamp TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

# --- Users / Login ---
def verify_login(user, pwd):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (user,))
    result = cursor.fetchone()
    conn.close()
    return result and result[0] == pwd

def update_password(user, new_pwd):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password = ? WHERE username = ?", (new_pwd, user))
    conn.commit()
    conn.close()

# --- Readers ---
def add_reader(full_name, inv_card, reg_date):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Если инвентарный номер не ввели, генерируем дефолтный на основе текущего времени
    if not inv_card:
        inv_card = "R-" + datetime.now().strftime("%M%S")
    if not reg_date:
        reg_date = datetime.now().strftime("%d.%m.%Y")
        
    cursor.execute('''
        INSERT INTO readers (inv_card, full_name, reg_date, books_current, books_read) 
        VALUES (?, ?, ?, 0, 0)
    ''', (inv_card, full_name, reg_date))
    conn.commit()
    conn.close()
    # Логируем
    log_transaction(inv_card, "-", full_name, "Новый читатель")
def get_all_readers():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, full_name, books_current, books_read FROM readers')
    rows = cursor.fetchall()
    conn.close()
    return rows

# --- Books ---
def add_book(inv_number, title, author, genre, place):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO books (inv_number, title, author, genre, place) 
        VALUES (?, ?, ?, ?, ?)
    ''', (inv_number, title, author, genre, place))
    conn.commit()
    conn.close()
    log_transaction(inv_number, title, "-", "Новая книга")

def get_all_books():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT inv_number, title, author, genre, status, place FROM books')
    rows = cursor.fetchall()
    conn.close()
    return rows

# ==========================================
# --- Dashboard & Transactions Logic ---
# ==========================================

def log_transaction(inv_number, book_title, reader_name, action_type):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M") 
    cursor.execute('''
        INSERT INTO transactions (inv_number, book_title, reader_name, action_type, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (inv_number, book_title, reader_name, action_type, time_now))
    conn.commit()
    conn.close()

def get_weekly_activity():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT strftime('%w', timestamp), COUNT(*) 
        FROM transactions 
        WHERE timestamp >= date('now', '-7 days')
        GROUP BY strftime('%w', timestamp)
    ''')
    rows = cursor.fetchall()
    conn.close()
    
    counts = [0, 0, 0, 0, 0, 0, 0]
    for row in rows:
        day_idx = int(row[0])
        if day_idx == 0:
            counts[6] = row[1] 
        else:
            counts[day_idx - 1] = row[1] 
    return counts

def get_recent_transactions(limit=5):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT inv_number, book_title, reader_name, action_type, substr(timestamp, 12, 5) FROM transactions ORDER BY id DESC LIMIT ?', (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_dashboard_stats():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM books WHERE status = 'Выдана'")
    books_out = cursor.fetchone()[0]
    
    overdue = 0
    
    cursor.execute("SELECT COUNT(*) FROM readers")
    total_readers = cursor.fetchone()[0]
    
    conn.close()
    return books_out, overdue, total_readers

def get_book_by_inv(inv_number):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT title, status FROM books WHERE inv_number = ?", (inv_number,))
    res = cursor.fetchone()
    conn.close()
    return res 

def get_reader_by_id(reader_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT full_name FROM readers WHERE id = ?", (reader_id,))
    res = cursor.fetchone()
    conn.close()
    return res[0] if res else None

def process_issue_db(inv_number, title, reader_id, reader_name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE books SET status = 'Выдана' WHERE inv_number = ?", (inv_number,))
    cursor.execute("UPDATE readers SET books_current = books_current + 1 WHERE id = ?", (reader_id,))
    conn.commit()
    conn.close()
    log_transaction(inv_number, title, reader_name, "Выдача")

def process_return_db(inv_number, title, reader_id, reader_name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE books SET status = 'В наличии' WHERE inv_number = ?", (inv_number,))
    cursor.execute("UPDATE readers SET books_current = MAX(0, books_current - 1), books_read = books_read + 1 WHERE id = ?", (reader_id,))
    conn.commit()
    conn.close()
    log_transaction(inv_number, title, reader_name, "Возврат")

def search_books(query):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    search_term = f"%{query}%"
    cursor.execute('''
        SELECT inv_number, title, author, genre, status, place 
        FROM books 
        WHERE title LIKE ? OR author LIKE ? OR inv_number LIKE ?
    ''', (search_term, search_term, search_term))
    rows = cursor.fetchall()
    conn.close()
    return rows

def search_readers(query):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    search_term = f"%{query}%"
    cursor.execute('''
        SELECT id, full_name, books_current, books_read 
        FROM readers 
        WHERE full_name LIKE ? OR id LIKE ?
    ''', (search_term, search_term))
    rows = cursor.fetchall()
    conn.close()
    return rows

# ==========================================
# --- REPORTING LOGIC (НОВЫЙ КОД ДЛЯ ОТЧЕТОВ) ---
# ==========================================

def get_available_months():
    """Ищет в транзакциях все месяцы, в которые происходили действия"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT substr(timestamp, 1, 7) FROM transactions ORDER BY timestamp")
    rows = cursor.fetchall()
    conn.close()

    months = []
    for row in rows:
        if row[0]: # Формат YYYY-MM
            y, m = row[0].split('-')
            months.append(f"{RU_MONTHS[m]} {y}")
            
    # Если база пока пустая, возвращаем текущий месяц
    if not months:
        curr_m = datetime.now().strftime("%m")
        curr_y = datetime.now().strftime("%Y")
        return [f"{RU_MONTHS[curr_m]} {curr_y}"]
        
    return months

def get_reports_data(start_str, end_str):
    """Собирает реальную статистику за выбранный диапазон времени"""
    try:
        # Превращаем "Март 2025" обратно в "2025-03-01"
        sm_name, sy = start_str.split()
        em_name, ey = end_str.split()
        start_date = f"{sy}-{RU_MONTHS_REV[sm_name]}-01"
        end_date = f"{ey}-{RU_MONTHS_REV[em_name]}-31 23:59:59"
    except:
        start_date = "1970-01-01"
        end_date = "2999-12-31"

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 1. ВСЕГО ВЫДАНО
    cursor.execute('''
        SELECT COUNT(*) FROM transactions 
        WHERE action_type = 'Выдача' AND timestamp BETWEEN ? AND ?
    ''', (start_date, end_date))
    total_issued = cursor.fetchone()[0]

    # 2. НОВЫХ КНИГ
    cursor.execute('''
        SELECT COUNT(*) FROM transactions 
        WHERE action_type = 'Новая книга' AND timestamp BETWEEN ? AND ?
    ''', (start_date, end_date))
    new_books = cursor.fetchone()[0]

    # 3. НОВЫХ ЧИТАТЕЛЕЙ
    cursor.execute('''
        SELECT COUNT(*) FROM transactions 
        WHERE action_type = 'Новый читатель' AND timestamp BETWEEN ? AND ?
    ''', (start_date, end_date))
    new_readers = cursor.fetchone()[0]

    # 4. ПОПУЛЯРНЫЕ ЖАНРЫ
    cursor.execute('''
        SELECT b.genre, COUNT(*) as c
        FROM transactions t
        JOIN books b ON t.inv_number = b.inv_number
        WHERE t.action_type = 'Выдача' AND t.timestamp BETWEEN ? AND ?
        GROUP BY b.genre
        ORDER BY c DESC LIMIT 4
    ''', (start_date, end_date))
    genres = cursor.fetchall()
    if not genres:
        genres = [("Нет данных", 1)]

    # 5. АКТИВНЫЕ И БРОСИВШИЕ ЧИТАТЕЛИ
    # Активные = те, кто брал или сдавал книги в этот период
    cursor.execute('''
        SELECT COUNT(DISTINCT reader_name) FROM transactions 
        WHERE action_type IN ('Выдача', 'Возврат') AND timestamp BETWEEN ? AND ?
    ''', (start_date, end_date))
    active_readers = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM readers')
    total_db_readers = cursor.fetchone()[0]
    inactive_readers = max(0, total_db_readers - active_readers)

    # 6. ДАННЫЕ ДЛЯ ГИСТОГРАММЫ (Динамика выдач)
    cursor.execute('''
        SELECT COUNT(*) FROM transactions 
        WHERE action_type = 'Выдача' AND timestamp BETWEEN ? AND ?
        GROUP BY substr(timestamp, 1, 10)
        ORDER BY timestamp DESC LIMIT 6
    ''', (start_date, end_date))
    hist_rows = cursor.fetchall()
    histogram = [r[0] for r in hist_rows]
    # Заполняем нулями, если данных мало
    while len(histogram) < 6:
        histogram.append(0)
    histogram.reverse()

    conn.close()

    return {
        "total_issued": total_issued,
        "histogram": histogram,
        "new_books": new_books,
        "new_readers": new_readers,
        "genres": genres,
        "active_readers": active_readers,
        "inactive_readers": inactive_readers
    }
def fix_existing_table():
    import sqlite3
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    try:
        # Добавляем колонку инвентарного номера билета
        cursor.execute("ALTER TABLE readers ADD COLUMN inv_card TEXT UNIQUE;")
        # Добавляем колонку даты регистрации
        cursor.execute("ALTER TABLE readers ADD COLUMN reg_date TEXT;")
        conn.commit()
        print("База данных успешно обновлена новые колонки добавлены!")
    except sqlite3.OperationalError as e:
        print("Колонки уже существуют или произошла ошибка:", e)
    finally:
        conn.close()

# Раскомментируй строчку ниже, запусти database.py один раз, а затем сотри её:
# fix_existing_table()

def add_book(inv_number, title, author, genre, place):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO books (inv_number, title, author, genre, place) 
        VALUES (?, ?, ?, ?, ?)
    ''', (inv_number, title, author, genre, place))
    conn.commit()
    conn.close()
    
    # Это триггерит появление во вкладке "Последние действия" и на графиках отчетов!
    log_transaction(inv_number, title, "-", "Новая книга")
