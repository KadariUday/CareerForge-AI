"""
Per-user rate limiting middleware using in-memory sliding window.
Falls back gracefully — never blocks users if limiter fails.
"""
import time
import logging
from collections import defaultdict, deque
from typing import Callable

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from ..config.settings import settings

logger = logging.getLogger(__name__)


class RateLimiter:
    """
    Sliding-window rate limiter.
    Tracks request timestamps per user/IP in a deque.
    """
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        # key → deque of timestamps
        self._windows: dict[str, deque] = defaultdict(deque)

    def is_allowed(self, key: str) -> tuple[bool, int]:
        """
        Returns (allowed: bool, remaining: int).
        Purges old timestamps from the window.
        """
        now = time.time()
        window_start = now - self.window_seconds
        dq = self._windows[key]

        # Remove expired timestamps
        while dq and dq[0] < window_start:
            dq.popleft()

        if len(dq) >= self.max_requests:
            remaining = 0
            return False, remaining

        dq.append(now)
        remaining = self.max_requests - len(dq)
        return True, remaining


# Global limiter instance
_limiter = RateLimiter(
    max_requests=settings.RATE_LIMIT_REQUESTS,
    window_seconds=settings.RATE_LIMIT_WINDOW_SECONDS,
)

# AI-specific stricter limiter (to reduce OpenAI costs)
_ai_limiter = RateLimiter(
    max_requests=20,  # 20 AI calls per hour per user
    window_seconds=3600,
)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Middleware that applies rate limiting per user (via JWT sub) or IP.
    Returns 429 with Retry-After header if limit exceeded.
    Soft-fail: if any error occurs, the request passes through.
    """

    # Paths that bypass rate limiting
    EXEMPT_PATHS = {"/", "/health", "/docs", "/redoc", "/openapi.json"}

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if request.url.path in self.EXEMPT_PATHS:
            return await call_next(request)

        allowed = True
        remaining = 0
        limit = settings.RATE_LIMIT_REQUESTS
        key = "unknown"

        try:
            # Identify user by JWT sub or by IP
            key = self._get_identifier(request)

            # AI endpoints get stricter limit
            if "/ai/" in request.url.path or request.url.path in {
                "/api/career/analyze", "/api/resume/analyze", "/api/chat/message"
            }:
                allowed, remaining = _ai_limiter.is_allowed(f"ai:{key}")
                limit = 20
            else:
                allowed, remaining = _limiter.is_allowed(key)
                limit = settings.RATE_LIMIT_REQUESTS

        except Exception as e:
            logger.error(f"Rate limiter error (passing through): {e}")
            allowed = True
            remaining = 0

        if not allowed:
            logger.warning(f"Rate limit exceeded for key: {key}")
            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Rate limit exceeded. Please wait before making more requests.",
                    "limit": limit,
                    "window_seconds": settings.RATE_LIMIT_WINDOW_SECONDS,
                },
                headers={
                    "Retry-After": str(settings.RATE_LIMIT_WINDOW_SECONDS),
                    "X-RateLimit-Limit": str(limit),
                    "X-RateLimit-Remaining": "0",
                },
            )

        response = await call_next(request)
        try:
            response.headers["X-RateLimit-Limit"] = str(limit)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
        except Exception:
            pass
        return response

    def _get_identifier(self, request: Request) -> str:
        """
        Extract user identifier from Authorization header (JWT sub)
        or fall back to client IP.
        """
        try:
            auth = request.headers.get("Authorization", "")
            if auth.startswith("Bearer "):
                from jose import jwt as _jwt
                token = auth.split(" ")[1]
                payload = _jwt.decode(
                    token,
                    settings.SECRET_KEY,
                    algorithms=[settings.ALGORITHM],
                    options={"verify_exp": False},
                )
                return f"user:{payload.get('sub', 'unknown')}"
        except Exception:
            pass

        # Fallback: IP address
        forwarded = request.headers.get("X-Forwarded-For")
        ip = forwarded.split(",")[0] if forwarded else request.client.host
        return f"ip:{ip}"
