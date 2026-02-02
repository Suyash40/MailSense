import imaplib
import email
from email.header import decode_header
from bs4 import BeautifulSoup


# Gmail IMAP server
IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993

class EmailReaderAgent:
    def __init__(self, email_user, email_pass):
        self.email_user = email_user
        self.email_pass = email_pass

    def fetch_emails(self, limit=20):
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(self.email_user, self.email_pass)
        mail.select("inbox")

        status, messages = mail.search(None, "ALL")
        email_ids = messages[0].split()

        latest_ids = email_ids[-limit:]

        emails_data = []

        for eid in latest_ids:
            res, msg = mail.fetch(eid, "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    msg_obj = email.message_from_bytes(response[1])

                    subject, encoding = decode_header(msg_obj["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")

                    sender = msg_obj.get("From")

                    body = ""

                    if msg_obj.is_multipart():
                        for part in msg_obj.walk():

                            content_type = part.get_content_type()

                            if content_type == "text/plain":
                                body = part.get_payload(decode=True).decode(errors="ignore")
                                break

                            elif content_type == "text/html":
                                html = part.get_payload(decode=True).decode(errors="ignore")
                                soup = BeautifulSoup(html, "html.parser")
                                body = soup.get_text(separator="\n")

                    else:
                        payload = msg_obj.get_payload(decode=True).decode(errors="ignore")

    # If HTML convert to text
                        if "<html" in payload.lower():
                            soup = BeautifulSoup(payload, "html.parser")
                            body = soup.get_text(separator="\n")
                        else:
                            body = payload


                    emails_data.append({
                        "subject": subject,
                        "from": sender,
                        "body": body[:800]  # limit for now
                    })

        mail.logout()
        return emails_data
