"""
MongoDB async connection using Motor (async MongoDB driver).
Provides a singleton client and collection accessors.
"""
import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional
from .settings import settings

logger = logging.getLogger(__name__)

# Singleton client
_client: Optional[AsyncIOMotorClient] = None
_db: Optional[AsyncIOMotorDatabase] = None


async def connect_db() -> None:
    """Initialize MongoDB connection on app startup."""
    global _client, _db
    try:
        _client = AsyncIOMotorClient(
            settings.MONGODB_URL,
            serverSelectionTimeoutMS=5000,
            maxPoolSize=50,  # Connection pool for concurrent users
            minPoolSize=5,
        )
        _db = _client[settings.DATABASE_NAME]
        # Verify connection
        await _client.admin.command("ping")
        logger.info(f"✅ Connected to MongoDB: {settings.DATABASE_NAME}")

        # Create indexes for performance
        await _create_indexes()
    except Exception as e:
        logger.error(f"❌ MongoDB connection failed: {e}")
        # Don't crash — allow app to run with degraded DB
        _client = None
        _db = None


async def disconnect_db() -> None:
    """Close MongoDB connection on app shutdown."""
    global _client
    if _client:
        _client.close()
        logger.info("MongoDB connection closed.")


def get_db() -> Optional[AsyncIOMotorDatabase]:
    """Return the active database instance."""
    return _db


async def _create_indexes() -> None:
    """Create MongoDB indexes for performance optimization."""
    if _db is None:
        return
    try:
        # Users: unique email index
        await _db.users.create_index("email", unique=True)
        await _db.users.create_index("created_at")

        # Resumes: user_id + created_at compound index
        await _db.resumes.create_index([("user_id", 1), ("created_at", -1)])

        # Career results: user_id index
        await _db.career_results.create_index([("user_id", 1), ("created_at", -1)])

        # Chat history: user_id index
        await _db.chat_history.create_index([("user_id", 1), ("created_at", -1)])

        # College data: exam + state compound index
        await _db.college_data.create_index([("exam", 1), ("state", 1)])
        await _db.college_data.create_index("cutoff_rank")

        logger.info("✅ MongoDB indexes created/verified.")
    except Exception as e:
        logger.warning(f"Index creation warning: {e}")
