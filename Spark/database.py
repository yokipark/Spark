import sqlite3

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
    
    # 2. Books Table (NEW!)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            inv_number TEXT NOT NULL,
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
    
    # Create a default user if none exists
    cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('admin', '1234')")
    
    conn.commit()
    conn.close()

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
    
    
# --- Reader Functions ---
def add_reader(full_name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO readers (full_name, books_current, books_read) VALUES (?, 0, 0)', (full_name,))
    conn.commit()
    conn.close()

def get_all_readers():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, full_name, books_current, books_read FROM readers')
    rows = cursor.fetchall()
    conn.close()
    return rows

# --- Book Functions (NEW!) ---
def add_book(inv_number, title, author, genre, place):
    """Adds a new book with the default status 'В наличии' (In Stock)"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO books (inv_number, title, author, genre, place) 
        VALUES (?, ?, ?, ?, ?)
    ''', (inv_number, title, author, genre, place))
    conn.commit()
    conn.close()

def get_all_books():
    """Fetches books in the exact column order needed for the UI table"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Note the order matches the headers: Inv No, Title, Author, Genre, Status, Place
    cursor.execute('SELECT inv_number, title, author, genre, status, place FROM books')
    rows = cursor.fetchall()
    conn.close()
    return rows
