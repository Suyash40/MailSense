from fastapi import APIRouter
import requests
from app.db import conn

router = APIRouter()

@router.post("/auth/google")
def google_login(data: dict):

    token = data["access_token"]

    # Fetch user email
    res = requests.get(
        "https://www.googleapis.com/oauth2/v2/userinfo",
        headers={"Authorization": f"Bearer {token}"}
    )

    user_info = res.json()
    email = user_info["email"]

    cursor = conn.cursor()

    # Save/update user
    cursor.execute("""
        INSERT OR REPLACE INTO users (email, access_token)
        VALUES (?, ?)
    """, (email, token))

    conn.commit()

    return {
        "email": email
    }
