from fastapi import APIRouter, HTTPException
from app.models import LeadRequest
from app.utils import save_lead
from app.logger import logger

router = APIRouter()

@router.post("/lead")
def capture_lead(lead: LeadRequest):
    """Capture lead details from frontend."""
    logger.info(f"📥 Lead API called — name={lead.name}, email={lead.email}, company={lead.company}")

    try:
        save_lead(lead.name, lead.email, lead.company)
        logger.info(f"💾 Lead successfully saved for {lead.email}")
        return {"message": "Lead saved successfully"}
    except Exception as e:
        logger.error(f"❌ Lead saving failed for {lead.email}: {e}")
        raise HTTPException(status_code=500, detail="Failed to save lead")
