"""
Pydantic models for Resume Analyzer module.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime


class ResumeSection(BaseModel):
    """Parsed section from resume."""
    name: str  # e.g. "Experience", "Education"
    content: str
    word_count: int


class ResumeAnalysisRequest(BaseModel):
    """Optional job description to compare resume against."""
    job_description: Optional[str] = Field(
        default=None,
        description="Paste job description to compare against resume"
    )
    target_role: Optional[str] = Field(
        default=None,
        description="Target job role e.g. 'Data Scientist'"
    )


class ATSScore(BaseModel):
    overall: float  # 0-100
    formatting: float
    keywords: float
    experience: float
    education: float
    skills: float


class ResumeSuggestion(BaseModel):
    category: str  # "Critical" | "Important" | "Nice-to-have"
    issue: str
    suggestion: str
    section: Optional[str] = None


class ResumeAnalysisResult(BaseModel):
    ats_score: ATSScore
    extracted_sections: List[ResumeSection]
    detected_skills: List[str]
    missing_keywords: List[str]
    suggestions: List[ResumeSuggestion]
    strengths: List[str]
    word_count: int
    has_contact_info: bool
    has_linkedin: bool
    has_github: bool
    improved_summary: Optional[str] = None
    ai_review: Optional[str] = None
    source: str = "ai"
    generated_at: datetime = Field(default_factory=datetime.utcnow)


class ResumeInDB(BaseModel):
    """Stored in MongoDB resumes collection."""
    user_id: str
    filename: str
    file_path: str
    raw_text: str
    analysis: Optional[Dict] = None
    job_description: Optional[str] = None
    target_role: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
