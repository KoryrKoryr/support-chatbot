import os
from dotenv import load_dotenv

load_dotenv()

print("SMTP_SERVER:", os.getenv("SMTP_SERVER"))
print("SMTP_PORT:", os.getenv("SMTP_PORT"))
print("ALERT_EMAIL:", os.getenv("ALERT_EMAIL"))
print("RECEIVER_EMAIL:", os.getenv("RECEIVER_EMAIL"))