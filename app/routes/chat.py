from fastapi import APIRouter, HTTPException
from app.models import ChatRequest
from app.utils import load_faqs, find_faq_answer
from app.logger import logger, chat_logger

router = APIRouter()

@router.post("/chat")
def chat(request: ChatRequest):
    """Chatbot endpoint that returns an FAQ answer if found."""
    chat_logger.info(f"💬 Chat request received: '{request.query}'")

    try:
        faqs = load_faqs()
        answer = find_faq_answer(request.query, faqs)

        if answer:
            chat_logger.info(f"🤖 Chatbot found FAQ answer for: '{request.query}'")
            return {"answer": answer}

        chat_logger.warning(f"⚠️ No FAQ match found for: '{request.query}'")
        return {"answer": "I'll connect you to our human support team."}

    except Exception as e:
        chat_logger.error(f"❌ Chat endpoint error: {e}")
        raise HTTPException(status_code=500, detail="Chat service unavailable")