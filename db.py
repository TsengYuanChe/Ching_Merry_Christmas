import sqlite3

DB_NAME = "angry_gpt.db"

def fetch_history(limit=5):
    """從資料庫中讀取最近的對話歷史"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT user_message, reply_message, timestamp FROM messages ORDER BY timestamp DESC LIMIT ?",
        (limit,)
    )
    history = cursor.fetchall()
    conn.close()
    return history

def save_to_db(user_message, reply_message):
    """儲存用戶訊息與回覆到資料庫"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO messages (user_message, reply_message, timestamp)
        VALUES (?, ?, datetime('now'))
    """, (user_message, reply_message))
    conn.commit()
    conn.close()

def search_message_in_history(message):
    """按訊息內容搜尋歷史"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT timestamp FROM messages WHERE user_message = ?
    """, (message,))
    results = cursor.fetchall()
    conn.close()
    return [result[0] for result in results]  # 返回所有匹配的時間戳