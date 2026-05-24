"""
Pydantic models for AI Chat Assistant module.
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timezone
from enum import Enum


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatMessage(BaseModel):
    role: MessageRole
    content: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    session_id: Optional[str] = Field(
        default=None,
        description="Session ID to maintain conversation context"
    )
    context: Optional[str] = Field(
        default=None,
        description="Optional context: 'career' | 'college' | 'resume' | 'general'"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "message": "What are the best careers after completing BDS?",
                "context": "career"
            }
        }


class ChatResponse(BaseModel):
    reply: str
    session_id: str
    suggestions: List[str] = []  # Follow-up question suggestions
    source: str = "ai"
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ChatSessionInDB(BaseModel):
    """Stored in MongoDB chat_history collection."""
    user_id: str
    session_id: str
    messages: List[ChatMessage] = []
    context: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
