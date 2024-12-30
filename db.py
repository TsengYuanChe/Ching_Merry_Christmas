import sqlite3

DB_NAME = "angry_gpt.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT NOT NULL,
            reply_message TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_to_db(user_message, reply_message):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO messages (user_message, reply_message, timestamp)
        VALUES (?, ?, datetime('now'))
    """, (user_message, reply_message))
    conn.commit()
    conn.close()

def search_message_in_history(message):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp FROM messages WHERE user_message = ?", (message,))
    results = cursor.fetchall()
    conn.close()
    return [row[0] for row in results]