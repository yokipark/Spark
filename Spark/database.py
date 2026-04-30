import sqlite3

DB_NAME = "library.db"

def init_db():
    """Creates the database and tables if they don't exist yet."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Create Readers Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS readers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            books_current INTEGER DEFAULT 0,
            books_read INTEGER DEFAULT 0
        )
    ''')
    
    conn.commit()
    conn.close()

def add_reader(full_name):
    """Inserts a new reader into the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO readers (full_name, books_current, books_read) 
        VALUES (?, 0, 0)
    ''', (full_name,))
    
    conn.commit()
    conn.close()

def get_all_readers():
    """Fetches all readers from the database to display in the table."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, full_name, books_current, books_read FROM readers')
    rows = cursor.fetchall()
    
    conn.close()
    return rows
