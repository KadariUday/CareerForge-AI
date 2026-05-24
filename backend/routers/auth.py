"""Auth router: signup, login, profile."""
import logging
from datetime import timedelta
from fastapi import APIRouter, HTTPException, status, Depends

from ..config.settings import settings
from ..models.user import UserRegister, UserLogin, TokenResponse, UserResponse, UpdateProfile
from ..services.auth_service import (
    verify_password, create_access_token, get_user_by_email,
    create_user, user_doc_to_response, get_current_user, get_user_by_id,
)
from ..config.database import get_db
from bson import ObjectId

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(data: UserRegister):
    """Register a new user and return JWT token."""
    user_doc = await create_user(data.name, data.email, data.password, data.role)
    user_response = user_doc_to_response(user_doc)
    token = create_access_token(
        {"sub": str(user_doc["_id"]), "email": data.email},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return TokenResponse(access_token=token, user=user_response)


@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin):
    """Authenticate user and return JWT token."""
    user_doc = await get_user_by_email(data.email)
    if not user_doc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")


    if not verify_password(data.password, user_doc["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    if not user_doc.get("is_active", True):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account deactivated")

    user_response = user_doc_to_response(user_doc)
    token = create_access_token(
        {"sub": str(user_doc["_id"]), "email": data.email},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    logger.info(f"User logged in: {data.email}")
    return TokenResponse(access_token=token, user=user_response)


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: UserResponse = Depends(get_current_user)):
    """Get the currently authenticated user's profile."""
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_profile(
    data: UpdateProfile,
    current_user: UserResponse = Depends(get_current_user),
):
    """Update the current user's profile fields."""
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database unavailable")

    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No update data provided")

    from datetime import datetime, timezone
    update_data["updated_at"] = datetime.now(timezone.utc)

    await db.users.update_one(
        {"_id": ObjectId(current_user.id)},
        {"$set": update_data}
    )
    updated_doc = await get_user_by_id(current_user.id)
    return user_doc_to_response(updated_doc)
