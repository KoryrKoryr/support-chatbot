from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import chat, lead, escalate
from app.utils import start_faq_watcher  # To auto-reload FAQ changes
from app.config import FAQ_PATH, ALERT_EMAIL
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
    """Initialize chatbot backend and verify all required files/configs."""
    print("\n🚀 Starting Support Chatbot Backend...\n")

    # 1️⃣ Verify FAQ CSV file
    if os.path.exists(FAQ_PATH):
        print(f"📄 FAQ file found at: {FAQ_PATH}")
    else:
        print(f"⚠️ FAQ file missing at: {FAQ_PATH}. Please add 'faq.csv' before testing.")

    # 2️⃣ Start FAQ file watcher (auto reload on edit)
    try:
        start_faq_watcher()
        print("👀 FAQ file watcher started successfully.")
    except Exception as e:
        print(f"❌ Failed to start FAQ watcher: {e}")

    # 3️⃣ Ensure leads.csv exists
    if not os.path.exists("leads.csv"):
        with open("leads.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["name", "email", "company"])
        print("🧾 Created new leads.csv file.")
    else:
        print("💾 leads.csv already exists — ready to store leads.")

    # 4️⃣ Check email escalation configuration
    if ALERT_EMAIL:
        print(f"📧 Email escalation is configured. Sending from: {ALERT_EMAIL}")
    else:
        print("⚠️ ALERT_EMAIL missing in .env — escalation emails will fail!")

    print("\n✅ Backend initialization complete — ready to serve!\n")


@app.get("/")
def root():
    """Health check endpoint."""
    return {"message": "Support Chatbot API is running 🚀"}
