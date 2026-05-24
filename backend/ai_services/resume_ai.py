"""
Resume Analyzer AI Service.
Pipeline: PDF extract → parse sections → ATS score → AI review (with fallback).
"""
import re
import logging
import io
import hashlib
from typing import Optional, List, Dict, Tuple

from ..config.settings import settings
from ..services.cache_service import cache_get, cache_set, make_cache_key
from ..models.resume import ResumeAnalysisResult, ATSScore, ResumeSection, ResumeSuggestion

logger = logging.getLogger(__name__)

ALL_KEYWORDS = [
    "python","java","javascript","typescript","c++","react","angular","vue","django",
    "fastapi","flask","spring","express","nodejs","mysql","postgresql","mongodb",
    "redis","aws","azure","gcp","docker","kubernetes","git","github","tensorflow",
    "pytorch","scikit-learn","pandas","numpy","linux","bash","agile","scrum",
    "communication","leadership","teamwork","sql","rest","api","html","css",
]

SECTION_PATTERNS = {
    "experience": r"(?i)(work\s*experience|experience|employment)",
    "education": r"(?i)(education|academic|qualification)",
    "skills": r"(?i)(skills|technical\s*skills|core\s*competencies|technologies)",
    "projects": r"(?i)(projects|personal\s*projects)",
    "summary": r"(?i)(summary|objective|profile|about\s*me)",
    "certifications": r"(?i)(certifications?|courses?|training)",
    "achievements": r"(?i)(achievements?|awards?|accomplishments?)",
}


def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text via pdfplumber, fallback to PyPDF2."""
    text = ""
    try:
        import pdfplumber
        with pdfplumber.open(io.BytesIO(file_content)) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text += t + "\n"
        if text.strip():
            return text
    except Exception as e:
        logger.warning(f"pdfplumber failed: {e}")
    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(io.BytesIO(file_content))
        for page in reader.pages:
            text += (page.extract_text() or "") + "\n"
    except Exception as e:
        logger.error(f"PyPDF2 failed: {e}")
    return text


def parse_sections(text: str) -> List[ResumeSection]:
    sections, current_section, current_content = [], "general", []
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue
        matched = None
        for name, pattern in SECTION_PATTERNS.items():
            if re.search(pattern, line) and len(line) < 60:
                matched = name
                break
        if matched:
            if current_content:
                c = "\n".join(current_content)
                sections.append(ResumeSection(name=current_section, content=c, word_count=len(c.split())))
            current_section, current_content = matched, []
        else:
            current_content.append(line)
    if current_content:
        c = "\n".join(current_content)
        sections.append(ResumeSection(name=current_section, content=c, word_count=len(c.split())))
    return sections


def detect_skills(text: str) -> Tuple[List[str], List[str]]:
    text_lower = text.lower()
    detected = [kw for kw in ALL_KEYWORDS if kw in text_lower]
    common = ["git", "python", "sql", "linux", "communication"]
    missing = [kw for kw in common if kw not in text_lower]
    return detected, missing


def compute_ats_score(text: str, sections: List[ResumeSection],
                      detected_skills: List[str], job_description: Optional[str] = None) -> ATSScore:
    text_lower = text.lower()
    word_count = len(text.split())
    section_names = {s.name for s in sections}

    formatting = 50.0
    if word_count > 300: formatting += 15
    if word_count > 500: formatting += 10
    if len(sections) >= 4: formatting += 15
    if re.search(r"\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*\b", text_lower): formatting += 10
    formatting = min(formatting, 100)

    keyword_score = min(len(detected_skills) * 5, 80)
    if job_description:
        jd_words = set(job_description.lower().split())
        resume_words = set(text_lower.split())
        overlap = len(jd_words & resume_words) / max(len(jd_words), 1)
        keyword_score = min(keyword_score + overlap * 20, 100)

    experience = 50.0
    if "experience" in section_names:
        exp = next((s for s in sections if s.name == "experience"), None)
        if exp and exp.word_count > 100: experience += 30
        if re.search(r"\d+\s*(year|yr|month)", text_lower): experience += 20
    experience = min(experience, 100)

    education = 50.0
    if "education" in section_names: education += 30
    if re.search(r"\b(b\.?tech|m\.?tech|bsc|msc|mbbs|bca|be|me|mba)\b", text_lower): education += 20
    education = min(education, 100)

    skills_sc = 40.0
    if "skills" in section_names: skills_sc += 30
    skills_sc += min(len(detected_skills) * 3, 30)
    skills_sc = min(skills_sc, 100)

    overall = formatting*0.2 + keyword_score*0.3 + experience*0.2 + education*0.15 + skills_sc*0.15

    return ATSScore(overall=round(overall,1), formatting=round(formatting,1),
                    keywords=round(keyword_score,1), experience=round(experience,1),
                    education=round(education,1), skills=round(skills_sc,1))


def generate_suggestions(text: str, sections: List[ResumeSection],
                          ats: ATSScore, missing: List[str]):
    suggestions, strengths = [], []
    section_names = {s.name for s in sections}

    if not re.search(r"\b[\w.]+@[\w.]+\.\w+\b", text):
        suggestions.append(ResumeSuggestion(category="Critical", issue="No email address",
            suggestion="Add a professional email at the top.", section="contact"))
    if "experience" not in section_names:
        suggestions.append(ResumeSuggestion(category="Critical", issue="No Experience section",
            suggestion="Add Work Experience section with internships or projects.", section="experience"))
    if "skills" not in section_names:
        suggestions.append(ResumeSuggestion(category="Critical", issue="No Skills section",
            suggestion="Add a dedicated Skills section.", section="skills"))
    if missing:
        suggestions.append(ResumeSuggestion(category="Important",
            issue=f"Missing keywords: {', '.join(missing[:5])}",
            suggestion="Add these keywords naturally in your resume.", section="skills"))
    if len(text.split()) < 300:
        suggestions.append(ResumeSuggestion(category="Important", issue="Resume too short",
            suggestion="Expand to 400-600 words with more details.", section="general"))
    if "linkedin" not in text.lower():
        suggestions.append(ResumeSuggestion(category="Important", issue="No LinkedIn URL",
            suggestion="Add LinkedIn profile URL.", section="contact"))
    if "github" not in text.lower():
        suggestions.append(ResumeSuggestion(category="Nice-to-have", issue="No GitHub URL",
            suggestion="Add GitHub profile to showcase code.", section="contact"))

    if "projects" in section_names: strengths.append("✅ Has Projects section")
    if "certifications" in section_names: strengths.append("✅ Includes certifications")
    if re.search(r"\d+\s*%|\d+\s*(users?|customers?|growth)", text, re.I):
        strengths.append("✅ Uses quantified achievements")
    if len(sections) >= 5: strengths.append("✅ Well-structured resume")

    return suggestions, strengths


async def analyze_resume(file_content: bytes, filename: str,
                          job_description: Optional[str] = None,
                          target_role: Optional[str] = None,
                          user_id: str = "anonymous") -> ResumeAnalysisResult:
    """Main resume analysis with caching."""
    file_hash = hashlib.md5(file_content).hexdigest()
    jd_hash = hashlib.md5((job_description or "").encode()).hexdigest()[:8]
    cache_key = make_cache_key("resume", file_hash, jd_hash)

    cached = await cache_get(cache_key)
    if cached:
        cached["source"] = "cached"
        return ResumeAnalysisResult(**cached)

    raw_text = extract_text_from_pdf(file_content) or "Could not extract text."
    sections = parse_sections(raw_text)
    detected_skills, missing_keywords = detect_skills(raw_text)
    contact_info_text = raw_text.lower()
    ats_score = compute_ats_score(raw_text, sections, detected_skills, job_description)
    suggestions, strengths = generate_suggestions(raw_text, sections, ats_score, missing_keywords)

    ai_review, improved_summary, source = None, None, "rule_based"

    if settings.AI_ENABLED and settings.OPENAI_API_KEY:
        try:
            ai_review, improved_summary = await _ai_resume_review(raw_text, job_description, target_role)
            source = "ai"
        except Exception as e:
            logger.error(f"AI resume review failed: {e}")

    result = ResumeAnalysisResult(
        ats_score=ats_score, extracted_sections=sections,
        detected_skills=detected_skills, missing_keywords=missing_keywords,
        suggestions=suggestions, strengths=strengths,
        word_count=len(raw_text.split()),
        has_contact_info=bool(re.search(r"\b[\w.]+@[\w.]+\.\w+\b", raw_text)),
        has_linkedin="linkedin" in contact_info_text,
        has_github="github" in contact_info_text,
        improved_summary=improved_summary, ai_review=ai_review, source=source,
    )
    await cache_set(cache_key, result.model_dump(), ttl=86400)
    return result


async def _ai_resume_review(resume_text: str, job_description: Optional[str],
                              target_role: Optional[str]) -> Tuple[str, Optional[str]]:
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(model=settings.OPENAI_MODEL, openai_api_key=settings.OPENAI_API_KEY,
                     max_tokens=600, temperature=0.3)
    jd_part = f"\nJD: {job_description[:400]}" if job_description else ""
    role_part = f"\nTarget Role: {target_role}" if target_role else ""
    prompt = f"""Review this resume. Respond with:
REVIEW: [3-sentence professional review]
IMPROVED_SUMMARY: [2-sentence improved objective/summary]

Resume (first 1500 chars):
{resume_text[:1500]}{jd_part}{role_part}"""
    resp = await llm.ainvoke(prompt)
    content = resp.content
    review, summary = content, None
    if "REVIEW:" in content:
        parts = content.split("IMPROVED_SUMMARY:")
        review = parts[0].replace("REVIEW:", "").strip()
        if len(parts) > 1:
            summary = parts[1].strip()
    return review[:500], summary
