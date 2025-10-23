from pydantic import BaseModel, EmailStr

class ChatRequest(BaseModel):
    query: str

class LeadRequest(BaseModel):
    name: str
    email: EmailStr
    company: str = ""

class EscalationRequest(BaseModel):
    question: str
    name: str
    email: EmailStr