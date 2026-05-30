import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

DB_FILE = os.getenv("DB_FILE", "contacts.db")

def get_connection():
    return sqlite3.connect(DB_FILE)

def setup_database():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS groups (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            name     TEXT NOT NULL,
            phone    TEXT,
            email    TEXT,
            group_id INTEGER REFERENCES groups(id)
        )
    """)
    conn.commit()
    conn.close()

