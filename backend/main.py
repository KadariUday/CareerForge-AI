"""
CareerForge AI — FastAPI Backend Entry Point
Wires together all routers, middleware, startup/shutdown lifecycle.
"""
import sys
import os
import logging
from contextlib import asynccontextmanager
from pathlib import Path

# Add project root to path so ai_services can be imported
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

from config.settings import settings
from config.database import connect_db, disconnect_db
from services.cache_service import init_cache
from middleware.rate_limiter import RateLimitMiddleware
from routers import auth_router, career_router, college_router, resume_router, chat_router, contact_router

# ─── Logging Setup ────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger("careerforge")


# ─── App Lifecycle ────────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown lifecycle manager."""
    logger.info(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")

    # Connect to MongoDB
    await connect_db()

    # Initialize cache (Redis or in-memory)
    await init_cache()

    # Ensure upload directory exists
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    logger.info("✅ All services initialized. Ready to serve.")
    yield

    # Shutdown
    await disconnect_db()
    logger.info("👋 Application shutdown complete.")


# ─── FastAPI App ──────────────────────────────────────────────────────────────
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
**CareerForge AI** — Unified intelligent platform for:
- 🎯 AI Career Guidance
- 🏫 College Predictor (NEET/JEE/EAMCET)
- 📄 Resume Analyzer (ATS Scoring)
- 💬 AI Chat Assistant
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# ─── CORS ─────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Rate Limiting ────────────────────────────────────────────────────────────
app.add_middleware(RateLimitMiddleware)

# ─── Static Files ─────────────────────────────────────────────────────────────
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# ─── Routers ──────────────────────────────────────────────────────────────────
app.include_router(auth_router)
app.include_router(career_router)
app.include_router(college_router)
app.include_router(resume_router)
app.include_router(chat_router)
app.include_router(contact_router)


# ─── Health & Root ────────────────────────────────────────────────────────────
@app.get("/", tags=["Root"])
async def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for load balancers and monitoring."""
    from config.database import get_db
    db_status = "connected" if get_db() is not None else "disconnected"
    return JSONResponse(content={
        "status": "healthy",
        "database": db_status,
        "ai_enabled": settings.AI_ENABLED,
        "environment": settings.ENVIRONMENT,
    })


# ─── Global Exception Handler ─────────────────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error. Please try again later."},
    )


if __name__ == "__main__":
    import uvicorn
    # Dynamically read the port environment variable from Render
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=settings.DEBUG,
        workers=1 if settings.DEBUG else 4,
    )

