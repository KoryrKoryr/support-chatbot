from fastapi import APIRouter
from app.models import ChatRequest
from app.utils import load_faqs, find_faq_answer

router = APIRouter()

@router.post("/chat")
def chat_endpoint(request: ChatRequest):
    """
    Handles chatbot queries.
    Returns FAQ answer if found, else fallback message.
    """
    faqs = load_faqs()
    answer = find_faq_answer(request.query, faqs)
    if answer:
        return {"response": answer, "confident": True}
    return {"response": "I'll connect you to our human support team.", "confident": False}
