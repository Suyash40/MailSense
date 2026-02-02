import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class EmailClassifierAgent:

    def classify(self, subject, body):

        prompt = f"""
You are an intelligent email classification system.

Classify the email into ONLY ONE of these categories:

urgent = security alerts, account issues, immediate action required  
job = job offers, interview emails, recruiter messages  
bill = invoices, payments, receipts, subscriptions  
spam = promotional emails, marketing, ads, offers, newsletters, scams, fake warnings  
normal = personal or general non-urgent emails  

Email Subject:
{subject}

Email Body:
{body}

Rules:
- If the email is promotional, marketing, newsletter, or offer → choose spam
- If the email looks fake, scammy, or suspicious → choose spam
- If it is a real security alert needing action → choose urgent

Respond with ONLY the category name.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        category = response.choices[0].message.content.strip().lower()

        return category
