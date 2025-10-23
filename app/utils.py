import csv, ssl, smtplib, threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from app.config import FAQ_PATH, SMTP_SERVER, SMTP_PORT, ALERT_EMAIL, ALERT_PASS
from app.logger import logger

#FAQ loading with Auto-Loading

_faq_cache = []        # Stores FAQs in memory
_cache_lock = threading.Lock()  # Prevents race conditions between reads/writes


def _load_faq_file():
    """Internal helper to safely read the FAQ CSV file."""
    faqs = []
    with open(FAQ_PATH, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row.get("question") or not row.get("answer"):
                continue
            faqs.append({
                "question": row["question"].strip(),
                "answer": row["answer"].strip(),
            })
    return faqs


def load_faqs():
    """
    Returns the cached FAQ data.
    Automatically loads from disk if cache is empty.
    """
    with _cache_lock:
        if not _faq_cache:
            _faq_cache.extend(_load_faq_file())
            logger.info(f"✅ Loaded {len(_faq_cache)} FAQs from file.")
    return _faq_cache


class FAQFileChangeHandler(FileSystemEventHandler):
    """Watchdog event handler to reload FAQ data on file changes."""

    def on_modified(self, event):
        if event.src_path.endswith("faq.csv"):
            logger.info("📄 Detected change in faq.csv — reloading FAQs...")
            try:
                new_data = _load_faq_file()
                with _cache_lock:
                    _faq_cache.clear()
                    _faq_cache.extend(new_data)
                logger.info(f"✅ Reloaded {len(new_data)} FAQs from file.")
            except Exception as e:
                logger.warning(f"⚠️ Failed to reload FAQs: {e}")


def start_faq_watcher():
    """Start a background thread that watches the FAQ file for changes."""
    observer = Observer()
    handler = FAQFileChangeHandler()
    observer.schedule(handler, str(Path(FAQ_PATH).parent), recursive=False)
    observer.daemon = True  # Stops when app shuts down
    observer.start()


# Start watcher automatically when module imports
start_faq_watcher()


# Simple Keyword search for FAQ answers

def find_faq_answer(query: str, faqs: list):
    """Find a matching answer from FAQ using simple keyword search."""
    logger.info(f"🔍 Received query: '{query}' — searching FAQs.")
    query_lower = query.lower()
    for faq in faqs:
        if any(word in faq["question"].lower() for word in query_lower.split()):
            return faq["answer"]
    logger.info("🤖 No direct FAQ match found, escalation may be needed.")
    return None


# Lead Capture

def save_lead(name, email, company):
    """Append lead information to leads.csv."""
    with open("leads.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([name, email, company])
    logger.info(f"💾 Lead saved: {name}, {email}, {company}")


# Email Escalation

def send_escalation_email(question, name, email):
    """Send email alert when chatbot cannot answer (UTF-8 safe)."""
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
    logger.info(f"📧 Escalation email sent for: {name} ({email})")
