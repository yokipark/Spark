import sqlite3
from datetime import datetime # Needed to get the current time

DB_NAME = "library.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. Readers Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS readers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            books_current INTEGER DEFAULT 0,
            books_read INTEGER DEFAULT 0
        )
    ''')
    
    # 2. Books Table (Notice: inv_number is now UNIQUE)
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
    
    # 3. Users Table (Login)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('admin', '1234')")

    # 4. Transactions Table (NEW!)
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
def add_reader(full_name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO readers (full_name, books_current, books_read) VALUES (?, 0, 0)', (full_name,))
    conn.commit()
    conn.close()
    # Log it for the graph!
    log_transaction("-", "-", full_name, "Новый читатель")


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
    # Log it for the graph!
    log_transaction(inv_number, title, "-", "Новая книга")

def get_all_books():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT inv_number, title, author, genre, status, place FROM books')
    rows = cursor.fetchall()
    conn.close()
    return rows

# ==========================================
# --- NEW: Dashboard & Transactions Logic ---
# ==========================================

def log_transaction(inv_number, book_title, reader_name, action_type):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Now saving Year-Month-Day Hour:Minute
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M") 
    cursor.execute('''
        INSERT INTO transactions (inv_number, book_title, reader_name, action_type, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (inv_number, book_title, reader_name, action_type, time_now))
    conn.commit()
    conn.close()

def get_weekly_activity():
    """Returns an array of 7 numbers representing actions from Mon to Sun"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # SQLite strftime('%w') gets the day of the week (0=Sunday, 1=Monday...)
    cursor.execute('''
        SELECT strftime('%w', timestamp), COUNT(*) 
        FROM transactions 
        WHERE timestamp >= date('now', '-7 days')
        GROUP BY strftime('%w', timestamp)
    ''')
    rows = cursor.fetchall()
    conn.close()
    
    # Empty week array: [Mon, Tue, Wed, Thu, Fri, Sat, Sun]
    counts = [0, 0, 0, 0, 0, 0, 0]
    for row in rows:
        day_idx = int(row[0])
        if day_idx == 0:
            counts[6] = row[1] # Sunday goes to the end of the array
        else:
            counts[day_idx - 1] = row[1] # Mon-Sat
            
    return counts

def get_recent_transactions(limit=5):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # We use substr() to only send "HH:MM" to the UI table so it doesn't look messy
    cursor.execute('SELECT inv_number, book_title, reader_name, action_type, substr(timestamp, 12, 5) FROM transactions ORDER BY id DESC LIMIT ?', (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_dashboard_stats():
    """Returns a tuple: (books_on_hand, overdue_count, new_readers)"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. Books on hand (Status = 'Выдана')
    cursor.execute("SELECT COUNT(*) FROM books WHERE status = 'Выдана'")
    books_out = cursor.fetchone()[0]
    
    # 2. Overdue (Placeholder 0 for now)
    overdue = 0
    
    # 3. Total Readers
    cursor.execute("SELECT COUNT(*) FROM readers")
    total_readers = cursor.fetchone()[0]
    
    conn.close()
    return books_out, overdue, total_readers


def get_book_by_inv(inv_number):
    """Returns the book title if it exists, otherwise None."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT title, status FROM books WHERE inv_number = ?", (inv_number,))
    res = cursor.fetchone()
    conn.close()
    return res # Returns tuple: (title, status)

def get_reader_by_id(reader_id):
    """Returns the reader's name if it exists, otherwise None."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT full_name FROM readers WHERE id = ?", (reader_id,))
    res = cursor.fetchone()
    conn.close()
    return res[0] if res else None

def process_issue_db(inv_number, title, reader_id, reader_name):
    """Updates database for issuing a book."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE books SET status = 'Выдана' WHERE inv_number = ?", (inv_number,))
    cursor.execute("UPDATE readers SET books_current = books_current + 1 WHERE id = ?", (reader_id,))
    conn.commit()
    conn.close()
    log_transaction(inv_number, title, reader_name, "Выдача")

def process_return_db(inv_number, title, reader_id, reader_name):
    """Updates database for returning a book."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE books SET status = 'В наличии' WHERE inv_number = ?", (inv_number,))
    cursor.execute("UPDATE readers SET books_current = MAX(0, books_current - 1), books_read = books_read + 1 WHERE id = ?", (reader_id,))
    conn.commit()
    conn.close()
    log_transaction(inv_number, title, reader_name, "Возврат")



# Search 

def search_books(query):
    """Поиск книг по названию, автору или инвентарному номеру."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # % означает "любой текст до или после запроса"
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
    """Поиск читателей по имени или ID."""
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
