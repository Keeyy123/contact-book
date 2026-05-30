import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("PG_HOST", "localhost"),
        port=os.getenv("PG_PORT", 5432),
        dbname=os.getenv("PG_NAME", "contactbook"),
        user=os.getenv("PG_USER", "contactuser"),
        password=os.getenv("PG_PASSWORD", "contactpass")
    )

def setup_database():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS groups (
            id   SERIAL PRIMARY KEY,
            name TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id       SERIAL PRIMARY KEY,
            name     TEXT NOT NULL,
            phone    TEXT,
            email    TEXT,
            group_id INTEGER REFERENCES groups(id)
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

