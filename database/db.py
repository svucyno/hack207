import sqlite3
import datetime
import os

DB_DIR = "db"
DB_PATH = os.path.join(DB_DIR, "history.db")

def init_db():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT,
            result TEXT,
            score REAL,
            timestamp TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_behavior (
            user_id INTEGER PRIMARY KEY,
            typing_baseline REAL,
            mouse_baseline REAL,
            click_baseline REAL
        )
    ''')
    
    # Insert default user 1 if not exists
    cursor.execute("INSERT OR IGNORE INTO user_behavior (user_id, typing_baseline, mouse_baseline, click_baseline) VALUES (1, 65, 220, 40)")
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blocked_files (
            file_hash TEXT PRIMARY KEY,
            original_name TEXT,
            blocked_path TEXT,
            timestamp TEXT
        )
    ''')
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='scans'")
    if cursor.fetchone():
        cursor.execute("INSERT INTO history (file_name, result, score, timestamp) SELECT file_name, result, score, timestamp FROM scans")
        cursor.execute("DROP TABLE scans")

    conn.commit()
    conn.close()

def log_scan(file_name, result, score):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    tz = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO history (file_name, result, score, timestamp) VALUES (?, ?, ?, ?)", (file_name, result, score, tz))
    conn.commit()
    conn.close()

def get_history(limit=50):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM history ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    conn.close()
    return rows, columns

def get_all_history():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM history ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    conn.close()
    return rows, columns

def save_user_baseline(user_id=1, typing=65, mouse=220, clicks=40):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO user_behavior (user_id, typing_baseline, mouse_baseline, click_baseline)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            typing_baseline=excluded.typing_baseline,
            mouse_baseline=excluded.mouse_baseline,
            click_baseline=excluded.click_baseline
    ''', (user_id, typing, mouse, clicks))
    conn.commit()
    conn.close()

def get_user_baseline(user_id=1):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT typing_baseline, mouse_baseline, click_baseline FROM user_behavior WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def add_blocked_file(file_hash, original_name, blocked_path):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    tz = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        cursor.execute('''
            INSERT INTO blocked_files (file_hash, original_name, blocked_path, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (file_hash, original_name, blocked_path, tz))
        conn.commit()
    except sqlite3.IntegrityError:
        pass # Already blocked
    conn.close()

def is_file_blocked(file_hash):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp FROM blocked_files WHERE file_hash = ?", (file_hash,))
    row = cursor.fetchone()
    conn.close()
    return row is not None

def get_all_blocked_files():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT file_hash, original_name, blocked_path, timestamp FROM blocked_files ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    conn.close()
    return rows, columns
