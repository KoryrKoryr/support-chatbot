from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import chat, lead, escalate
from app.utils import start_faq_watcher  # To auto-reload FAQ changes
from app.config import FAQ_PATH, ALERT_EMAIL
from app.logger import logger  # import our logger
import os, csv


# Initialize FastAPI App
app = FastAPI(
    title="Support Chatbot API",
    version="1.0",
    description="Handles FAQs, lead capture, and escalation emails."
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For testing; replace with your frontend domain in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(chat.router, prefix="/api", tags=["Chat"])
app.include_router(lead.router, prefix="/api", tags=["Leads"])
app.include_router(escalate.router, prefix="/api", tags=["Escalation"])

# Startup Event — runs once at server boot
@app.on_event("startup")
async def startup_event():
    """Initialize chatbot backend and verify configurations."""
    logger.info("🚀 Starting Support Chatbot Backend...")

    # Verify FAQ file
    if os.path.exists(FAQ_PATH):
        logger.info(f"📄 FAQ file found at: {FAQ_PATH}")
    else:
        logger.warning(f"⚠️ FAQ file missing at {FAQ_PATH}. Please add 'faq.csv' before testing.")

    # Start FAQ watcher
    try:
        start_faq_watcher()
        logger.info("👀 FAQ watcher started successfully.")
    except Exception as e:
        logger.error(f"❌ Failed to start FAQ watcher: {e}")

    # Ensure leads.csv exists
    if not os.path.exists("leads.csv"):
        with open("leads.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["name", "email", "company"])
        logger.info("🧾 Created new leads.csv file.")
    else:
        logger.info("💾 leads.csv already exists — ready to store leads.")

    # Check email config
    if ALERT_EMAIL:
        logger.info(f"📧 Email escalation configured. Sending from: {ALERT_EMAIL}")
    else:
        logger.warning("⚠️ ALERT_EMAIL missing in .env — escalation emails will fail!")

    logger.info("✅ Backend initialization complete — ready to serve!")


@app.get("/")
def root():
    """Health check endpoint."""
    return {"message": "Support Chatbot API is running 🚀"}
