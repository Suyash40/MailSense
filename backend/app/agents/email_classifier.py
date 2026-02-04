import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class EmailClassifierAgent:

    def classify(self, subject, body):

        prompt = f"""
You are an expert email classification AI.

Your task is to classify the email into ONLY ONE of the following categories:

urgent  
job  
bill  
spam  
normal  

### CATEGORY DEFINITIONS:

urgent:
- security alerts
- suspicious login warnings
- password changes
- account access issues
- payment failures
- delivery problems
- anything that requires immediate action

job:
- job offers
- internship emails
- interview invitations
- recruiter messages
- application updates
- hiring process emails

bill:
- invoices
- payment confirmations
- subscription charges
- receipts
- bank statements

spam:
- promotional offers
- discounts
- marketing campaigns
- newsletters
- ads
- lottery winnings
- fake alerts
- scam-looking emails

normal:
- personal messages
- general updates
- non-urgent communication

---

### IMPORTANT RULES:

1. If it looks promotional or marketing → spam  
2. If it is a security or account warning → urgent  
3. If related to job/internship/hiring → job  
4. If related to money transactions → bill  
5. Otherwise → normal  

---

Email Subject:
{subject}

Email Body:
{body}

---

Respond with ONLY one word:
urgent, job, bill, spam, or normal
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
