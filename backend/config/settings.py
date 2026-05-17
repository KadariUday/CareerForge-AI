"""
Application settings loaded from environment variables.
Pydantic BaseSettings automatically reads from .env file.
"""
from pydantic_settings import BaseSettings
from pydantic import field_validator
from functools import lru_cache
from typing import Optional, Any
import os


class Settings(BaseSettings):
    # App
    APP_NAME: str = "CareerForge AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # MongoDB
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "careerforge"

    # OpenAI
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    OPENAI_MAX_TOKENS: int = 1500
    AI_ENABLED: bool = True  # Toggle to disable AI if quota exceeded

    # Redis (optional — falls back to in-memory cache)
    REDIS_URL: Optional[str] = None
    CACHE_TTL_SECONDS: int = 3600  # 1 hour

    # Rate limiting
    RATE_LIMIT_REQUESTS: int = 50
    RATE_LIMIT_WINDOW_SECONDS: int = 3600

    # File uploads
    MAX_UPLOAD_SIZE_MB: int = 10
    UPLOAD_DIR: str = "uploads"

    # CORS
    ALLOWED_ORIGINS: list = [
        "http://localhost:5173",
        "http://localhost:3000",
        "https://careerforge-ai.vercel.app",
    ]

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_origins(cls, v: Any) -> list:
        if isinstance(v, str):
            v = v.strip()
            # Handle JSON list
            if v.startswith("[") and v.endswith("]"):
                try:
                    import json
                    return json.loads(v)
                except Exception:
                    pass
            # Handle comma-separated list
            if "," in v:
                return [x.strip() for x in v.split(",") if x.strip()]
            # Handle single wildcard or string
            return [v]
        return v

    # Email (Optional — for Contact Form)
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    CONTACT_EMAIL: str = "kadariuday2233@gmail.com"

    class Config:
        env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Cached settings instance — loaded once per process."""
    return Settings()


settings = get_settings()
