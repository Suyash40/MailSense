from fastapi import APIRouter
from app.db import conn
from app.agents.gmail_reader import fetch_user_emails
from app.agents.agent_graph import build_graph
from datetime import datetime
from app.agents.summary_agent import SummaryAgent
from fastapi import Request


router = APIRouter()
graph = build_graph()

@router.get("/emails")
def get_emails(limit: int = 10, offset: int = 0):

    cursor = conn.cursor()

    cursor.execute("""
        SELECT email, access_token, gmail_page_token
        FROM users
        ORDER BY ROWID DESC LIMIT 1
    """)

    user = cursor.fetchone()

    if not user:
        return {"emails": []}

    email, token, page_token = user

    # 1️⃣ Try DB first
    cursor.execute("""
        SELECT subject, body, category, action_item
        FROM emails
        WHERE user_email = ?
        ORDER BY created_at DESC
        LIMIT ? OFFSET ?
    """, (email, limit, offset))

    rows = cursor.fetchall()

    if len(rows) == limit:
        return {
            "emails": [
                {
                    "subject": r[0],
                    "body": r[1],
                    "category": r[2],
                    "actions": {"task_created": r[3]}
                }
                for r in rows
            ]
        }

    # 2️⃣ Fetch next batch from Gmail
    gmail_emails, next_token = fetch_user_emails(
        token,
        max_results=limit,
        page_token=page_token
    )

    if not gmail_emails:
        return {"emails": []}

    result = graph.invoke({"emails": gmail_emails})
    processed = result["emails"]

    for mail in processed:
        cursor.execute("""
            INSERT OR IGNORE INTO emails
            (user_email, subject, body, category, action_item, created_at)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (
            email,
            mail["subject"],
            mail["body"],
            mail["category"],
            mail["actions"]["task_created"]
        ))

    # save cursor
    cursor.execute("""
        UPDATE users SET gmail_page_token = ?
        WHERE email = ?
    """, (next_token, email))

    conn.commit()

    return {"emails": processed}






@router.get("/emails/history")
def get_email_history():

    cursor = conn.cursor()

    cursor.execute("""
    SELECT subject, category
    FROM emails
    WHERE created_at >= datetime('now','start of day','localtime')
    """)


    rows = cursor.fetchall()

    emails = []

    for r in rows:
        emails.append({
            "subject": r[0],
            "body": r[1],
            "category": r[2],
            "actions": {
                "task_created": r[3]
            },
            "created_at": r[4]
        })

    return {"emails": emails}

@router.get("/summary/daily")
def daily_summary():

    cursor = conn.cursor()
    today = datetime.now().date().isoformat()

    # ✅ Check if summary already exists
    cursor.execute(
        "SELECT summary FROM daily_summaries WHERE date = ?",
        (today,)
    )

    existing = cursor.fetchone()

    if existing:
        return {"summary": existing[0]}   # ⚡ instant return


    # 🔄 Otherwise generate new

    cursor.execute("""
        SELECT subject, category
        FROM emails
        WHERE DATE(created_at) = ?
    """, (today,))

    rows = cursor.fetchall()

    if not rows:
        return {"summary": "No emails received today."}

    emails = [
        {"subject": r[0], "category": r[1]}
        for r in rows
    ]

    agent = SummaryAgent()
    summary = agent.generate_summary(emails)

    # 💾 Save summary
    cursor.execute("""
        INSERT OR REPLACE INTO daily_summaries (date, summary)
        VALUES (?, ?)
    """, (today, summary))


    conn.commit()

    return {"summary": summary}




@router.get("/debug/emails")
def debug_emails():
    cursor = conn.cursor()
    cursor.execute("SELECT subject, created_at FROM emails LIMIT 10")
    rows = cursor.fetchall()
    return {"rows": rows}

@router.get("/debug/users")
def debug_users():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return {"users": cursor.fetchall()}



