"""
AI Career Guidance Service.

Uses LangChain + OpenAI with:
  - Structured JSON output via prompt templates
  - Rule-based fallback when AI is disabled or API fails
  - Response caching to reduce API calls
"""
import json
import logging
import re
from typing import Optional
from datetime import datetime

from ..config.settings import settings
from ..services.cache_service import cache_get, cache_set, make_cache_key
from ..models.career import CareerInput, CareerOutput, CareerPath

logger = logging.getLogger(__name__)

# ─── Prompt Template ──────────────────────────────────────────────────────────

CAREER_PROMPT = """You are an expert career counselor for Indian students with deep knowledge of:
- Career paths in technology, medicine, law, arts, commerce, engineering
- Indian job market trends and salary insights
- Skill requirements and learning roadmaps

Given the student profile below, recommend exactly 4 career paths.
Return ONLY a valid JSON object — no explanation, no markdown.

Student Profile:
- Interests: {interests}
- Current Skills: {skills}
- Academic Scores: {scores}
- Personality Traits: {traits}
- Education Level: {education}
- Preferred Work Style: {work_style}

Return this exact JSON structure:
{{
  "career_paths": [
    {{
      "title": "Career Title",
      "description": "2-3 sentence description",
      "match_percentage": 85,
      "required_skills": ["skill1", "skill2"],
      "skills_to_learn": ["skill3", "skill4"],
      "average_salary_lpa": "8-15 LPA",
      "growth_rate": "High",
      "demand_level": "Very High",
      "top_companies": ["Company1", "Company2"],
      "recommended_courses": ["Course1", "Course2"],
      "timeline_months": 12
    }}
  ],
  "summary": "Overall assessment of the student",
  "immediate_action": "First concrete step to take"
}}"""

# ─── Rule-Based Fallback ──────────────────────────────────────────────────────

RULE_BASED_CAREERS = {
    "coding": [
        CareerPath(
            title="Software Engineer",
            description="Design and develop software systems. High demand across all industries.",
            match_percentage=90.0,
            required_skills=["Programming", "Data Structures", "System Design"],
            skills_to_learn=["Cloud Computing", "DevOps", "Microservices"],
            average_salary_lpa="8-30 LPA",
            growth_rate="High",
            demand_level="Very High",
            top_companies=["Google", "Microsoft", "Infosys", "TCS", "Flipkart"],
            recommended_courses=["DSA Masterclass", "System Design", "AWS Certification"],
            timeline_months=6,
        ),
        CareerPath(
            title="Data Scientist",
            description="Extract insights from data using ML and statistics.",
            match_percentage=82.0,
            required_skills=["Python", "Statistics", "Machine Learning"],
            skills_to_learn=["Deep Learning", "MLOps", "Big Data"],
            average_salary_lpa="10-25 LPA",
            growth_rate="High",
            demand_level="High",
            top_companies=["Amazon", "Walmart Labs", "Mu Sigma", "Fractal Analytics"],
            recommended_courses=["ML Specialization", "Deep Learning AI", "Kaggle competitions"],
            timeline_months=8,
        ),
    ],
    "biology": [
        CareerPath(
            title="Medical Doctor (MBBS/MD)",
            description="Diagnose and treat patients. Respected profession with stable demand.",
            match_percentage=88.0,
            required_skills=["Biology", "Chemistry", "Patient Care"],
            skills_to_learn=["Clinical Skills", "Medical Research", "Specialization"],
            average_salary_lpa="10-50+ LPA",
            growth_rate="Stable",
            demand_level="High",
            top_companies=["AIIMS", "Apollo Hospitals", "Fortis", "Government Hospitals"],
            recommended_courses=["NEET Preparation", "MBBS", "MD Specialization"],
            timeline_months=72,
        ),
        CareerPath(
            title="Bioinformatics Scientist",
            description="Bridge between biology and data science. Analyze genomic data.",
            match_percentage=78.0,
            required_skills=["Biology", "Python", "Statistics"],
            skills_to_learn=["Genomics", "R Programming", "Bioinformatics Tools"],
            average_salary_lpa="6-20 LPA",
            growth_rate="High",
            demand_level="Medium",
            top_companies=["CSIR", "Biocon", "Dr Reddy's", "TCS Life Sciences"],
            recommended_courses=["Bioinformatics Specialization", "R for Data Science"],
            timeline_months=18,
        ),
    ],
    "design": [
        CareerPath(
            title="UX/UI Designer",
            description="Design user experiences for digital products. Creative and technical role.",
            match_percentage=87.0,
            required_skills=["Visual Design", "User Research", "Figma/Sketch"],
            skills_to_learn=["Design Systems", "Prototyping", "Motion Design"],
            average_salary_lpa="6-20 LPA",
            growth_rate="High",
            demand_level="High",
            top_companies=["Swiggy", "Zomato", "Razorpay", "Design agencies"],
            recommended_courses=["Google UX Design Certificate", "Interaction Design"],
            timeline_months=6,
        ),
    ],
    "business": [
        CareerPath(
            title="Product Manager",
            description="Lead product strategy and work with engineering/design teams.",
            match_percentage=84.0,
            required_skills=["Communication", "Analytics", "Problem Solving"],
            skills_to_learn=["Product Strategy", "Data Analysis", "Agile/Scrum"],
            average_salary_lpa="12-35 LPA",
            growth_rate="High",
            demand_level="Very High",
            top_companies=["Flipkart", "Meesho", "Razorpay", "Amazon", "Zomato"],
            recommended_courses=["PM Bootcamp", "Google Analytics", "MBA"],
            timeline_months=12,
        ),
    ],
    "finance": [
        CareerPath(
            title="Investment Banker / Financial Analyst",
            description="Analyze financial markets, raise capital, and advise corporates.",
            match_percentage=85.0,
            required_skills=["Financial Modeling", "Excel", "Accounting"],
            skills_to_learn=["CFA", "Bloomberg", "M&A Analysis"],
            average_salary_lpa="8-40 LPA",
            growth_rate="Medium",
            demand_level="High",
            top_companies=["Goldman Sachs", "JP Morgan", "ICICI Bank", "Kotak"],
            recommended_courses=["CFA Level 1", "Financial Modeling Course"],
            timeline_months=18,
        ),
    ],
}

DEFAULT_CAREER = CareerPath(
    title="Management Consultant",
    description="Solve business problems for organizations across industries.",
    match_percentage=70.0,
    required_skills=["Analytical Thinking", "Communication", "Research"],
    skills_to_learn=["Case Study Solving", "Presentation Skills", "Data Visualization"],
    average_salary_lpa="8-25 LPA",
    growth_rate="Medium",
    demand_level="Medium",
    top_companies=["McKinsey", "BCG", "Deloitte", "KPMG"],
    recommended_courses=["MBA", "Case Interview Prep", "Excel Mastery"],
    timeline_months=24,
)


def _rule_based_career(career_input: CareerInput) -> CareerOutput:
    """Fallback: match interests to predefined career paths."""
    found_paths = []
    interests_lower = [i.lower() for i in career_input.interests]

    for interest in interests_lower:
        for keyword, paths in RULE_BASED_CAREERS.items():
            if keyword in interest or interest in keyword:
                for path in paths:
                    if path.title not in [p.title for p in found_paths]:
                        found_paths.append(path)

    if not found_paths:
        found_paths = [DEFAULT_CAREER]

    found_paths = found_paths[:4]

    return CareerOutput(
        career_paths=found_paths,
        summary=f"Based on your interests in {', '.join(career_input.interests[:3])}, "
                f"we've identified {len(found_paths)} career paths that could be a great fit.",
        immediate_action="Start by building foundational skills in your top interest area. "
                         "Explore online courses and talk to professionals in your target field.",
        source="rule_based",
    )


# ─── Main AI Service ──────────────────────────────────────────────────────────

async def analyze_career(career_input: CareerInput, user_id: str) -> CareerOutput:
    """
    Main entry point for career analysis.
    1. Check cache
    2. Try AI (LangChain + OpenAI)
    3. Fallback to rule-based
    """
    # Build cache key from input hash
    cache_key = make_cache_key(
        "career",
        sorted(career_input.interests),
        sorted(career_input.skills),
        career_input.current_education or "",
    )

    # Check cache
    cached = await cache_get(cache_key)
    if cached:
        logger.info(f"Career analysis cache hit for user {user_id}")
        cached["source"] = "cached"
        return CareerOutput(**cached)

    # Try AI if enabled
    if settings.AI_ENABLED and settings.OPENAI_API_KEY:
        try:
            result = await _ai_career_analysis(career_input)
            # Cache the result
            data = result.model_dump() if hasattr(result, "model_dump") else result.dict()
            await cache_set(cache_key, data, ttl=86400)  # 24h cache
            return result
        except Exception as e:
            logger.error(f"AI career analysis failed: {e}. Using rule-based fallback.")

    # Fallback
    result = _rule_based_career(career_input)
    data = result.model_dump() if hasattr(result, "model_dump") else result.dict()
    await cache_set(cache_key, data, ttl=3600)
    return result


async def _ai_career_analysis(career_input: CareerInput) -> CareerOutput:
    """Call LangChain + OpenAI for structured career recommendations."""
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import PromptTemplate
    from langchain_core.output_parsers import JsonOutputParser

    llm = ChatOpenAI(
        model=settings.OPENAI_MODEL,
        openai_api_key=settings.OPENAI_API_KEY,
        max_tokens=settings.OPENAI_MAX_TOKENS,
        temperature=0.7,
    )

    prompt = PromptTemplate.from_template(CAREER_PROMPT)
    chain = prompt | llm | JsonOutputParser()

    scores_str = ", ".join(
        f"{k}: {v}" for k, v in career_input.academic_scores.items()
    ) or "Not provided"

    result_dict = await chain.ainvoke({
        "interests": ", ".join(career_input.interests),
        "skills": ", ".join(career_input.skills) or "None listed",
        "scores": scores_str,
        "traits": ", ".join(career_input.personality_traits or []) or "Not specified",
        "education": career_input.current_education or "Not specified",
        "work_style": career_input.preferred_work_style or "Flexible",
    })

    # Parse career paths
    paths = [CareerPath(**cp) for cp in result_dict.get("career_paths", [])]
    return CareerOutput(
        career_paths=paths,
        summary=result_dict.get("summary", ""),
        immediate_action=result_dict.get("immediate_action", ""),
        source="ai",
    )
