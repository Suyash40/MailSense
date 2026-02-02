import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class EmailExtractorAgent:

    def extract_info(self, subject, body):

        prompt = f"""
You are an AI that extracts useful information from emails.

From the email below, extract:

1. deadline (if any, else null)
2. amount (if any, else null)
3. action_item (short task if any, else null)

Return ONLY in JSON format like:

{{
 "deadline": "...",
 "amount": "...",
 "action_item": "..."
}}

Email Subject:
{subject}

Email Body:
{body}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        result = response.choices[0].message.content.strip()

        return result
