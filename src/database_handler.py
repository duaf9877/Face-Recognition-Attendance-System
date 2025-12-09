# src/database_handler.py

import sqlite3
from datetime import datetime
import os

# Build absolute path to the database
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
DB_PATH = os.path.join(project_root, "attendance", "attendance.db")

def create_table():
    """Ensures the database and table exist."""
    db_dir = os.path.dirname(DB_PATH)
    os.makedirs(db_dir, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def mark_attendance(student_name, status="Present"):
    """Adds a new attendance record to the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")
    cursor.execute(
        "INSERT INTO attendance_records (student_name, date, time, status) VALUES (?, ?, ?, ?)",
        (student_name, date, time, status)
    )
    conn.commit()
    conn.close()
    print(f"[DB LOG] Marked '{student_name}' as {status} at {time}")

def get_all_attendance():
    """Fetches all attendance records from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT student_name, date, time, status FROM attendance_records ORDER BY id DESC")
    records = cursor.fetchall()
    conn.close()
    return records