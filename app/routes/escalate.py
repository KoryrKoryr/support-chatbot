from fastapi import APIRouter, HTTPException
from app.models import EscalationRequest
from app.utils import send_escalation_email
from app.logger import logger

router = APIRouter()

@router.post("/escalate")
def escalate_request(data: EscalationRequest):
    """Trigger an escalation email when chatbot cannot answer."""
    logger.info(f"🚨 Escalate API called by {data.email} — question='{data.question[:50]}...'")

    try:
        send_escalation_email(data.question, data.name, data.email)
        logger.info(f"📧 Escalation email sent to support for {data.email}")
        return {"message": "Escalation email sent successfully"}
    except Exception as e:
        logger.error(f"❌ Escalation email failed for {data.email}: {e}")
        raise HTTPException(status_code=500, detail="Failed to send escalation email")
