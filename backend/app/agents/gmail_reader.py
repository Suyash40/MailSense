import requests
import base64


def decode(data):
    return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")


def get_header(headers, name):
    for h in headers:
        if h["name"].lower() == name.lower():
            return h["value"]
    return ""


def extract_body(payload):

    if payload.get("body", {}).get("data"):
        return decode(payload["body"]["data"])

    if "parts" in payload:
        for part in payload["parts"]:

            if part["mimeType"] == "text/plain" and part["body"].get("data"):
                return decode(part["body"]["data"])

            if "parts" in part:
                for sub in part["parts"]:
                    if sub["mimeType"] == "text/plain" and sub["body"].get("data"):
                        return decode(sub["body"]["data"])

    return ""


def fetch_user_emails(token, max_results=20):

    headers = {
        "Authorization": f"Bearer {token}"
    }

    all_message_ids = []
    page_token = None

    # 1️⃣ Get message IDs (pagination)
    while len(all_message_ids) < max_results:

        params = {
            "maxResults": 20
        }

        if page_token:
            params["pageToken"] = page_token

        res = requests.get(
            "https://gmail.googleapis.com/gmail/v1/users/me/messages",
            headers=headers,
            params=params
        )
        print("RAW",res.text)

        data = res.json()
        
        messages = data.get("messages", [])
        print("TOTAL MESSAGES:", len(messages))

        if "messages" not in data:
            break

        all_message_ids.extend(data["messages"])
        page_token = data.get("nextPageToken")

        if not page_token:
            break

    # 2️⃣ Fetch full email content
    emails = []

    for msg in all_message_ids:

        msg_id = msg["id"]

        msg_res = requests.get(
            f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{msg_id}",
            headers=headers
        )

        data = msg_res.json()
        payload = data.get("payload", {})
        headers_list = payload.get("headers", [])

        subject = ""
        sender = ""

        for h in headers_list:
            if h["name"] == "Subject":
                subject = h["value"]
            if h["name"] == "From":
                sender = h["value"]

        body = ""

        parts = payload.get("parts", [])

        for part in parts:
            if part["mimeType"] == "text/plain":
                body_data = part["body"].get("data")
                if body_data:
                    body = base64.urlsafe_b64decode(body_data).decode(errors="ignore")

        emails.append({
            "subject": subject,
            "from": sender,
            "body": body
        })

        if len(emails) >= max_results:
            break

    print("TOTAL EMAILS FETCHED:", len(emails))

    return emails
