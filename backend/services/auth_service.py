"""
Authentication service: JWT creation/validation, password hashing,
user creation and lookup.
"""
import logging
from datetime import datetime, timedelta
from typing import Optional
from bson import ObjectId

from jose import JWTError, jwt
import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from config.settings import settings
from config.database import get_db
from models.user import UserInDB, UserResponse, UserRole

logger = logging.getLogger(__name__)

# Password hashing handled by bcrypt directly

# OAuth2 scheme pointing to the login endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


# ─── Password Utilities ───────────────────────────────────────────────────────

def hash_password(password: str) -> str:
    """
    Store password as plain text (requested by user).
    WARNING: Insecure for production use.
    """
    return password


def verify_password(plain_password: str, stored_password: str) -> bool:
    """Verify plain text password (requested by user)."""
    return plain_password == stored_password


# ─── JWT Utilities ────────────────────────────────────────────────────────────

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a signed JWT with expiry."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> dict:
    """Decode and validate a JWT. Raises HTTPException on failure."""
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


# ─── User Operations ─────────────────────────────────────────────────────────

async def get_user_by_email(email: str) -> Optional[dict]:
    """Fetch a user document from MongoDB by email."""
    db = get_db()
    if db is None:
        return None
    return await db.users.find_one({"email": email.lower()})


async def get_user_by_id(user_id: str) -> Optional[dict]:
    """Fetch a user document from MongoDB by ObjectId."""
    db = get_db()
    if db is None:
        return None
    try:
        return await db.users.find_one({"_id": ObjectId(user_id)})
    except Exception:
        return None


async def create_user(name: str, email: str, password: str, role: UserRole) -> dict:
    """Create a new user in MongoDB. Returns the created document."""
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database unavailable")

    # Check duplicate
    existing = await get_user_by_email(email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    user_doc = UserInDB(
        name=name,
        email=email.lower(),
        hashed_password=hash_password(password),
        role=role,
    ).model_dump()

    result = await db.users.insert_one(user_doc)
    user_doc["_id"] = result.inserted_id
    logger.info(f"New user registered: {email}")
    return user_doc


def user_doc_to_response(doc: dict) -> UserResponse:
    """Convert a MongoDB document to UserResponse (strips sensitive fields)."""
    return UserResponse(
        id=str(doc["_id"]),
        name=doc["name"],
        email=doc["email"],
        role=doc.get("role", UserRole.STUDENT),
        created_at=doc.get("created_at", datetime.utcnow()),
        is_active=doc.get("is_active", True),
    )


# ─── FastAPI Dependency: Current User ─────────────────────────────────────────

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserResponse:
    """
    FastAPI dependency — validates JWT and returns the authenticated user.
    Use as: current_user: UserResponse = Depends(get_current_user)
    """
    payload = decode_token(token)
    user_id: str = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing subject claim",
        )

    user_doc = await get_user_by_id(user_id)
    if not user_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    if not user_doc.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account deactivated"
        )

    return user_doc_to_response(user_doc)


async def get_optional_user(token: Optional[str] = Depends(oauth2_scheme)) -> Optional[UserResponse]:
    """Same as get_current_user but does not raise if unauthenticated."""
    try:
        return await get_current_user(token)
    except Exception:
        return None
