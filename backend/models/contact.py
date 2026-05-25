from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timezone

from typing import Optional

class ContactRequest(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    message: str

class ContactMessageInDB(ContactRequest):
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    processed: bool = False
