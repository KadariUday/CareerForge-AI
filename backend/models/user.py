
"""
Pydantic models for User authentication and profile management.
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime, timezone
from enum import Enum


class UserRole(str, Enum):
    STUDENT = "student"
    PROFESSIONAL = "professional"
    ADMIN = "admin"


# ─── Request/Response Models ──────────────────────────────────────────────────

class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: UserRole = UserRole.STUDENT

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Arjun Sharma",
                "email": "arjun@example.com",
                "password": "SecurePass123",
                "role": "student",
            }
        }


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    role: UserRole
    created_at: datetime
    is_active: bool = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class UserInDB(BaseModel):
    """Internal model with hashed password — never exposed via API."""
    name: str
    email: str
    hashed_password: str
    role: UserRole = UserRole.STUDENT
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    # Profile extras
    skills: List[str] = []
    interests: List[str] = []
    education: Optional[str] = None


class UpdateProfile(BaseModel):
    name: Optional[str] = None
    skills: Optional[List[str]] = None
    interests: Optional[List[str]] = None
    education: Optional[str] = None
