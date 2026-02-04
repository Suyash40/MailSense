import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class SummaryAgent:

    def generate_summary(self, emails):
        """
        emails = list of dicts like:
        [
          {"subject": "...", "category": "..."},
          ...
        ]
        """

        # Prepare readable content for AI
        content = "\n".join(
            f"- [{e['category']}] {e['subject']}"
            for e in emails
        )

        prompt = f"""
You are an intelligent email assistant.

Below are today's emails with their categories:

{content}

Create a clear daily summary including:

• How many emails arrived today  
• Important urgent alerts (if any)  
• Job or internship updates (if any)  
• Bills or payments (if any)  
• Overall pattern (mostly spam, mostly normal, etc.)

Keep it short, helpful, and easy to read.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        summary = response.choices[0].message.content.strip()

        return summary
