from dotenv import load_dotenv
import os
from pathlib import Path

# Load environment variables
load_dotenv()

#Path to the FAQ file
FAQ_PATH = Path(__file__).resolve().parent.parent / "faq.csv"

# SMTP email configuration (for escalation alerts)
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
ALERT_EMAIL = os.getenv("ALERT_EMAIL")
ALERT_PASS = os.getenv("ALERT_PASS")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL", ALERT_EMAIL)