"""AI Chat assistant router with session management."""
import logging
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from models.chat import ChatRequest, ChatResponse, ChatSessionInDB, ChatMessage, MessageRole
from models.user import UserResponse
from services.auth_service import get_current_user
from config.database import get_db
from ai_services import chat, clear_session

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/chat", tags=["AI Chat Assistant"])


async def _persist_message(user_id: str, session_id: str, role: str, content: str, context: str = None):
    """Append a message to the MongoDB chat history."""
    try:
        db = get_db()
        if db is None:
            return
        now = datetime.utcnow()
        message = {"role": role, "content": content, "timestamp": now}
        await db.chat_history.update_one(
            {"user_id": user_id, "session_id": session_id},
            {
                "$push": {"messages": message},
                "$set": {"updated_at": now, "context": context},
                "$setOnInsert": {"created_at": now},
            },
            upsert=True,
        )
    except Exception as e:
        logger.error(f"Chat persist error: {e}")


@router.post("/message", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
    current_user: UserResponse = Depends(get_current_user),
):
    """
    Send a message to the AI chat assistant.
    Maintains conversation context via session_id.
    """
    reply, session_id, suggestions = await chat(
        message=request.message,
        session_id=request.session_id,
        context=request.context,
        user_id=current_user.id,
    )

    # Persist to MongoDB (fire-and-forget style)
    try:
        await _persist_message(current_user.id, session_id, "user", request.message, request.context)
        await _persist_message(current_user.id, session_id, "assistant", reply, request.context)
    except Exception as e:
        logger.warning(f"Could not persist chat: {e}")

    return ChatResponse(reply=reply, session_id=session_id, suggestions=suggestions)


@router.get("/history")
async def get_chat_history(
    limit: int = 20,
    current_user: UserResponse = Depends(get_current_user),
):
    """Retrieve the user's recent chat sessions."""
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database unavailable")

    cursor = db.chat_history.find(
        {"user_id": current_user.id},
        {"session_id": 1, "context": 1, "updated_at": 1, "messages": {"$slice": -2}}
    ).sort("updated_at", -1).limit(limit)

    sessions = []
    async for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        sessions.append(doc)
    return {"sessions": sessions, "total": len(sessions)}


@router.delete("/session/{session_id}")
async def clear_chat_session(
    session_id: str,
    current_user: UserResponse = Depends(get_current_user),
):
    """Clear a specific chat session from memory and DB."""
    await clear_session(session_id)

    db = get_db()
    if db:
        await db.chat_history.delete_one({"user_id": current_user.id, "session_id": session_id})

    return {"message": "Session cleared"}
