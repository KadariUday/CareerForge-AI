from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timezone

class ContactRequest(BaseModel):
    name: str
    email: EmailStr
    phone: str
    message: str

class ContactMessageInDB(ContactRequest):
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    processed: bool = False
