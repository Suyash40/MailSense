import sqlite3

conn = sqlite3.connect("emails.db", check_same_thread=False)

def init_db():
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
    email TEXT PRIMARY KEY,
    access_token TEXT,
    gmail_page_token TEXT
    )
    """)


    # Emails table (DEDUPED)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS emails (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_email TEXT,
        subject TEXT,
        body TEXT,
        category TEXT,
        action_item TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        UNIQUE(user_email, subject, body)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS daily_summaries (
    date TEXT PRIMARY KEY,
    summary TEXT
    )
    """)


    conn.commit()

# Run once on startup
init_db()
