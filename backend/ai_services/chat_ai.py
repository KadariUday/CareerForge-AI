"""
AI Chat Assistant Service using LangChain with conversation memory.
Falls back to rule-based responses when AI is unavailable.
"""
import uuid
import logging
from typing import Optional, List, Dict
from ..config.settings import settings
from ..services.cache_service import cache_get, cache_set, make_cache_key
from ..models.chat import ChatMessage, MessageRole
from ..models.resume import ResumeAnalysisResult, ATSScore, ResumeSection, ResumeSuggestion

logger = logging.getLogger(__name__)

# In-memory session store (use Redis for production multi-instance)
_sessions: Dict[str, List[dict]] = {}

RULE_BASED_RESPONSES = {
    "bds": "After BDS, popular career options include: (1) MDS specialization in Orthodontics, Oral Surgery, or Prosthodontics, (2) Government dental officer roles, (3) Private dental clinic setup, (4) Healthcare management/MBA, (5) Dental product sales. MDS offers the highest earning potential (20-40 LPA for specialists).",
    "mbbs": "After MBBS: (1) MD/MS specialization — highest earning path, (2) Government medical officer (stable job), (3) USMLE for USA, PLAB for UK, (4) Public health/MPH, (5) Healthcare startup/MedTech. Specialize in high-demand fields like Radiology, Orthopedics, or Cardiology for best salaries.",
    "rank 25": "For NEET rank ~25,000 (General): Safe choices include government medical colleges in states like UP, Bihar, Rajasthan. Target: mid-tier private colleges like KIMS, Manipal (fees 15-25 LPA). Dream: top private colleges. Consider EAMCET in AP/Telangana for better options with state quota.",
    "rank 10": "For NEET rank ~10,000: Good chances at government medical colleges in most states. Target: VMMC Delhi, GMCH Chandigarh. You have strong options across India. Consider AIQ quota carefully.",
    "jee": "For JEE Mains rank ~50,000: Safe options include NITs in states with lower cutoffs (NIT Sikkim, NIT Nagaland). Target: mid-tier NITs. Dream: top NITs require rank under 15,000. Consider state engineering colleges and IIITs too.",
    "resume": "To improve your resume: (1) Quantify achievements (e.g., 'Improved performance by 40%'), (2) Use action verbs, (3) Add LinkedIn and GitHub links, (4) Keep to 1 page for <5 years experience, (5) Include a strong summary, (6) Tailor keywords to the job description.",
    "career after 12": "Top careers after 12th: Engineering (JEE), Medicine (NEET), Law (CLAT), CA/CMA, Design (NID/NIFT), Data Science (B.Sc), Management (BBA→MBA). Choose based on your strengths — PCM leads to engineering/tech; PCB to medicine; Commerce to finance/law.",
    "data scientist": "Becoming a Data Scientist: (1) Learn Python, SQL, Statistics, (2) Study ML (scikit-learn, TensorFlow), (3) Build 3-5 projects on Kaggle, (4) Get certified (Google, IBM Data Science), (5) Apply for data analyst roles first, transition to DS. Salary: 8-25 LPA in India.",
    "software engineer": "Software Engineering path: (1) Master DSA (LeetCode 200+ problems), (2) Learn System Design, (3) Pick a specialization (Backend/Frontend/Full-stack), (4) Build portfolio projects on GitHub, (5) Target product companies. Salary: 8-40 LPA depending on company tier.",
}

FOLLOW_UP_SUGGESTIONS = {
    "career": ["What skills should I learn?", "How long will it take?", "What are the salary expectations?"],
    "college": ["What are the fees?", "Which state has better cutoffs?", "What is the placement record?"],
    "resume": ["How to write a good summary?", "What keywords should I add?", "How to quantify achievements?"],
    "general": ["Tell me about career options", "Help me with college prediction", "Analyze my resume"],
}


def _rule_based_response(message: str, context: Optional[str]) -> tuple[str, List[str]]:
    """Pattern-match user message to predefined helpful responses."""
    msg_lower = message.lower()
    for keyword, response in RULE_BASED_RESPONSES.items():
        if keyword in msg_lower:
            suggestions = FOLLOW_UP_SUGGESTIONS.get(context or "general", FOLLOW_UP_SUGGESTIONS["general"])
            return response, suggestions
    
    default = ("I'm CareerForge AI, here to help with career guidance, college predictions, and resume analysis! "
                "Try asking: 'Best careers after 12th PCM', 'Colleges for NEET rank 30000', or 'How to improve my resume'.")
    return default, FOLLOW_UP_SUGGESTIONS["general"]


async def chat(message: str, session_id: Optional[str], context: Optional[str],
               user_id: str) -> tuple[str, str, List[str]]:
    """Process a chat message. Returns (reply, session_id, suggestions)."""
    if not session_id:
        session_id = str(uuid.uuid4())

    if session_id not in _sessions:
        _sessions[session_id] = []

    history = _sessions[session_id]
    history.append({"role": "user", "content": message})

    reply, suggestions = "", []

    if settings.AI_ENABLED and settings.OPENAI_API_KEY:
        try:
            reply, suggestions = await _ai_chat(message, history, context)
        except Exception as e:
            logger.error(f"AI chat failed: {e}. Using rule-based fallback.")
            reply, suggestions = _rule_based_response(message, context)
    else:
        reply, suggestions = _rule_based_response(message, context)

    history.append({"role": "assistant", "content": reply})
    # Keep last 20 messages to control token usage
    _sessions[session_id] = history[-20:]

    return reply, session_id, suggestions


async def _ai_chat(message: str, history: List[dict], context: Optional[str]) -> tuple[str, List[str]]:
    """LangChain-powered chat with conversation history."""
    from langchain_openai import ChatOpenAI
    from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

    llm = ChatOpenAI(model=settings.OPENAI_MODEL, openai_api_key=settings.OPENAI_API_KEY,
                     max_tokens=500, temperature=0.7)

    context_hint = {
        "career": "Focus on career guidance, job market trends, and skill development.",
        "college": "Focus on Indian college admissions, cutoff ranks, and entrance exams.",
        "resume": "Focus on resume improvement, ATS optimization, and job applications.",
    }.get(context or "", "Provide helpful guidance on career, education, and job preparation.")

    messages = [SystemMessage(content=f"""You are CareerForge AI, an expert career counselor for Indian students.
{context_hint}
Be concise (under 150 words), helpful, and specific. Use bullet points when listing options.""")]

    for msg in history[-8:]:  # Last 4 exchanges for context
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        else:
            messages.append(AIMessage(content=msg["content"]))

    resp = await llm.ainvoke(messages)
    reply = resp.content

    suggestions = FOLLOW_UP_SUGGESTIONS.get(context or "general", FOLLOW_UP_SUGGESTIONS["general"])
    return reply, suggestions


async def get_session_history(session_id: str) -> List[dict]:
    return _sessions.get(session_id, [])


async def clear_session(session_id: str) -> None:
    _sessions.pop(session_id, None)
