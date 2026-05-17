"""
Caching service with Redis primary and in-memory fallback.
Transparent to consumers — use get/set/delete regardless of backend.
"""
import json
import logging
import time
import hashlib
from typing import Any, Optional
from config.settings import settings

logger = logging.getLogger(__name__)

# ─── In-Memory Fallback ───────────────────────────────────────────────────────

class InMemoryCache:
    """Simple TTL-aware in-memory cache. Thread-safe enough for single-process."""
    def __init__(self):
        self._store: dict = {}  # key → (value, expiry_timestamp)

    def get(self, key: str) -> Optional[str]:
        entry = self._store.get(key)
        if entry is None:
            return None
        value, expiry = entry
        if time.time() > expiry:
            del self._store[key]
            return None
        return value

    def set(self, key: str, value: str, ttl: int = 3600) -> None:
        self._store[key] = (value, time.time() + ttl)

    def delete(self, key: str) -> None:
        self._store.pop(key, None)

    def clear(self) -> None:
        self._store.clear()

    def size(self) -> int:
        # Purge expired first
        now = time.time()
        expired = [k for k, (_, exp) in self._store.items() if now > exp]
        for k in expired:
            del self._store[k]
        return len(self._store)


# Singleton in-memory cache instance
_memory_cache = InMemoryCache()
_redis_client = None


# ─── Redis Initializer ────────────────────────────────────────────────────────

async def init_cache() -> None:
    """Try to connect to Redis; fall back to in-memory if unavailable."""
    global _redis_client
    if not settings.REDIS_URL:
        logger.info("No REDIS_URL configured — using in-memory cache.")
        return
    try:
        import redis.asyncio as redis
        _redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
        await _redis_client.ping()
        logger.info("✅ Redis cache connected.")
    except Exception as e:
        logger.warning(f"Redis unavailable ({e}) — falling back to in-memory cache.")
        _redis_client = None


# ─── Public Interface ─────────────────────────────────────────────────────────

async def cache_get(key: str) -> Optional[Any]:
    """Retrieve cached value (JSON-decoded). Returns None on miss."""
    try:
        if _redis_client:
            raw = await _redis_client.get(key)
        else:
            raw = _memory_cache.get(key)

        if raw is None:
            return None
        return json.loads(raw)
    except Exception as e:
        logger.warning(f"Cache GET error for key '{key}': {e}")
        return None


async def cache_set(key: str, value: Any, ttl: int = None) -> None:
    """Store a value in cache (JSON-encoded) with TTL."""
    ttl = ttl or settings.CACHE_TTL_SECONDS
    try:
        serialized = json.dumps(value, default=str)
        if _redis_client:
            await _redis_client.setex(key, ttl, serialized)
        else:
            _memory_cache.set(key, serialized, ttl)
    except Exception as e:
        logger.warning(f"Cache SET error for key '{key}': {e}")


async def cache_delete(key: str) -> None:
    """Remove a cache entry."""
    try:
        if _redis_client:
            await _redis_client.delete(key)
        else:
            _memory_cache.delete(key)
    except Exception as e:
        logger.warning(f"Cache DELETE error for key '{key}': {e}")


def make_cache_key(*args) -> str:
    """Generate a consistent cache key from arbitrary arguments."""
    raw = ":".join(str(a) for a in args)
    return "cf:" + hashlib.md5(raw.encode()).hexdigest()
