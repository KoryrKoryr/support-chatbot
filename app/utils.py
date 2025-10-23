import pandas as pd
import csv, ssl, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import FAQ_PATH, SMTP_SERVER, SMTP_PORT, ALERT_EMAIL, ALERT_PASS

def load_faqs():
    """
    Loads FAQ data from a CSV file safely.
    Handles commas, quotes, and encodings automatically.
    Returns a list of dictionaries with 'question' and 'answer' keys.
    """
    faqs = []
    try:
        with open(FAQ_PATH, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Skip blank rows or rows missing required fields
                if not row.get("question") or not row.get("answer"):
                    continue
                faqs.append({
                    "question": row["question"].strip(),
                    "answer": row["answer"].strip(),
                })
    except FileNotFoundError:
        raise FileNotFoundError(f"FAQ file not found at {FAQ_PATH}")
    except Exception as e:
        raise RuntimeError(f"Failed to load FAQ CSV: {e}")

    if not faqs:
        raise ValueError("FAQ file is empty or improperly formatted.")

    return faqs


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