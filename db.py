import sqlite3

# 資料庫名稱
DB_NAME = "angry_gpt.db"

# 初始化資料庫
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

# 建立資料庫連接
def connect_db():
    conn = sqlite3.connect(DB_NAME)
    return conn

# 儲存訊息與回覆到資料庫
def save_to_db(user_message, reply_message):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO messages (user_message, reply_message, timestamp)
        VALUES (?, ?, datetime('now'))
    """, (user_message, reply_message))
    conn.commit()
    conn.close()

# 從資料庫讀取歷史訊息
def fetch_history(limit=5):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT user_message, reply_message, timestamp
        FROM messages
        ORDER BY timestamp DESC
        LIMIT ?
    """, (limit,))
    history = cursor.fetchall()
    conn.close()
    return history

# 搜尋訊息是否出現在歷史記錄中
def search_message_in_history(message):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT timestamp FROM messages WHERE user_message = ?
    """, (message,))
    results = cursor.fetchall()
    conn.close()
    return [result[0] for result in results]  # 返回所有匹配的時間戳