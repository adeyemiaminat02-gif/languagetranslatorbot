import sqlite3
import aiofiles
from utils.config import DATABASE_URL
from utils.logger import logger

def init_db():
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        last_lang TEXT DEFAULT 'en'
    )""")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        source_text TEXT,
        translated_text TEXT,
        target_lang TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS favorites (
        user_id INTEGER,
        lang_code TEXT,
        PRIMARY KEY (user_id, lang_code)
    )""")
    
    conn.commit()
    conn.close()
    logger.info("Database initialized successfully.")

async def add_user(user_id: int, username: str):
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
    conn.commit()
    conn.close()

async def update_last_lang(user_id: int, lang_code: str):
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET last_lang = ? WHERE user_id = ?", (lang_code, user_id))
    conn.commit()
    conn.close()

async def get_user_last_lang(user_id: int) -> str:
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT last_lang FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else "en"

async def add_history(user_id: int, source: str, translated: str, target: str):
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO history (user_id, source_text, translated_text, target_lang) VALUES (?, ?, ?, ?)",
        (user_id, source, translated, target)
    )
    # Keep only last 10 entries per user
    cursor.execute("""
        DELETE FROM history WHERE id NOT IN (
            SELECT id FROM history WHERE user_id = ? ORDER BY timestamp DESC LIMIT 10
        ) AND user_id = ?
    """, (user_id, user_id))
    conn.commit()
    conn.close()

async def get_history(user_id: int):
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT source_text, translated_text, target_lang FROM history WHERE user_id = ? ORDER BY timestamp DESC LIMIT 10", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

async def add_favorite(user_id: int, lang_code: str):
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO favorites (user_id, lang_code) VALUES (?, ?)", (user_id, lang_code))
    conn.commit()
    conn.close()

async def remove_favorite(user_id: int, lang_code: str):
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM favorites WHERE user_id = ? AND lang_code = ?", (user_id, lang_code))
    conn.commit()
    conn.close()

async def get_favorites(user_id: int):
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT lang_code FROM favorites WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [r[0] for r in rows]
