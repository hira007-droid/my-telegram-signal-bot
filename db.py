# db.py
import sqlite3

def init_db():
    conn = sqlite3.connect("bot_database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pair TEXT,
            timeframe TEXT,
            direction TEXT,
            confidence INTEGER,
            result TEXT DEFAULT 'pending'
        )
    """)
    conn.commit()
    conn.close()

def get_setting(key, default=None):
    conn = sqlite3.connect("bot_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else default

def set_setting(key, value):
    conn = sqlite3.connect("bot_database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()

def save_signal(pair, timeframe, direction, confidence):
    conn = sqlite3.connect("bot_database.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO signals (pair, timeframe, direction, confidence)
        VALUES (?, ?, ?, ?)
    """, (pair, timeframe, direction, confidence))
    signal_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return signal_id

def set_result(signal_id, result):
    conn = sqlite3.connect("bot_database.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE signals SET result = ? WHERE id = ?", (result, signal_id))
    conn.commit()
    conn.close()