import sqlite3


def db_for_feed():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS feed (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        link TEXT UNIQUE,
        source TEXT,
        type TEXT,
        date TEXT,
        image TEXT
    )
    """)

    conn.commit()
    conn.close()
