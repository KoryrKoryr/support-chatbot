from fastapi import APIRouter
from app.models import LeadRequest
from app.utils import save_lead

router = APIRouter()

@router.post("/lead")
def save_lead_endpoint(lead: LeadRequest):
    """Saves a lead's details to CSV."""
    save_lead(lead.name, lead.email, lead.company)
    return {"message": "Lead captured successfully!"}
