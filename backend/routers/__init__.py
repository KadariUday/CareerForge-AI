from .auth import router as auth_router
from .career import router as career_router
from .college import router as college_router
from .resume import router as resume_router
from .chat import router as chat_router
from .contact import router as contact_router

__all__ = ["auth_router", "career_router", "college_router", "resume_router", "chat_router", "contact_router"]
