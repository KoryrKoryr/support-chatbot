import pandas as pd
import csv, ssl, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import FAQ_PATH, SMTP_SERVER, SMTP_PORT, ALERT_EMAIL, ALERT_PASS

def load_faqs():
    """Load FAQ data from a CSV file into a list of dictionaries."""
    df = pd.read_csv(FAQ_PATH)
    return df.to_dict(orient="records")


def find_faq_answer(query: str, faqs: list):
    """Find a matching answer from FAQ using simple keyword search."""
    query_lower = query.lower()
    for faq in faqs:
        if any(word in faq["question"].lower() for word in query_lower.split()):
            return faq["answer"]
    return None


def save_lead(name, email, company):
    """Append lead information to leads.csv."""
    with open("leads.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([name, email, company])


def send_escalation_email(question, name, email):
    """Send email alert when AI cannot answer (UTF-8 safe)."""
    msg = MIMEMultipart()
    msg["Subject"] = "Chatbot Escalation Needed ⚠️"
    msg["From"] = ALERT_EMAIL
    msg["To"] = ALERT_EMAIL

    body = f"""
A new support escalation occurred.

👤 Name: {name}
📧 Email: {email}
❓ Question: {question}
"""
    msg.attach(MIMEText(body, "plain", "utf-8"))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
        server.login(ALERT_EMAIL, ALERT_PASS)
        server.send_message(msg)