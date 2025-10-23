from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import chat, lead, escalate

app = FastAPI(title="Support Chatbot API", version="1.0")

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(chat.router, prefix="/api")
app.include_router(lead.router, prefix="/api")
app.include_router(escalate.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Support Chatbot API is running 🚀"}
