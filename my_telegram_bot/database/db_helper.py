import sqlite3
from threading import Lock

conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()
lock = Lock()

cursor.execute('''CREATE TABLE IF NOT EXISTS addresses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    address TEXT NOT NULL,
                    info TEXT NOT NULL,
                    added_info INTEGER DEFAULT 0
                )''')
conn.commit()

def get_address(address):
    with lock:
        cursor.execute("SELECT * FROM addresses WHERE address=?", (address,))
        return cursor.fetchone()

def add_address(address, info):
    with lock:
        cursor.execute("INSERT INTO addresses (address, info) VALUES (?, ?)", (address, info))
        conn.commit()

def update_address_info(address, info):
    with lock:
        cursor.execute("UPDATE addresses SET info = ? WHERE address = ?", (info, address))
        conn.commit()