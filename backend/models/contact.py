from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class ContactRequest(BaseModel):
    name: str
    email: EmailStr
    phone: str
    message: str

class ContactMessageInDB(ContactRequest):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    processed: bool = False
