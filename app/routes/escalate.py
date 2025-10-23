from fastapi import APIRouter
from app.models import EscalationRequest
from app.utils import send_escalation_email

router = APIRouter()

@router.post("/escalate")
def escalate_endpoint(data: EscalationRequest):
    """Triggers email escalation when AI can't answer."""
    send_escalation_email(data.question, data.name, data.email)
    return {"message": "Escalation email sent!"}
