"""
Pydantic models for the AI Career Guidance module.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class PersonalityTrait(str, Enum):
    ANALYTICAL = "analytical"
    CREATIVE = "creative"
    LEADERSHIP = "leadership"
    SOCIAL = "social"
    TECHNICAL = "technical"
    ENTREPRENEURIAL = "entrepreneurial"


class CareerInput(BaseModel):
    interests: List[str] = Field(..., min_items=1, max_items=10,
                                  description="Areas of interest e.g. ['coding', 'biology']")
    skills: List[str] = Field(default=[], description="Current skills")
    academic_scores: Dict[str, float] = Field(
        default={},
        description="Subject scores e.g. {'math': 85, 'physics': 90}"
    )
    personality_traits: Optional[List[PersonalityTrait]] = None
    current_education: Optional[str] = Field(None, description="e.g. '12th PCM', 'B.Tech CSE 3rd year'")
    preferred_work_style: Optional[str] = Field(None, description="Remote / On-site / Hybrid")
    budget_for_education: Optional[str] = Field(None, description="e.g. 'Under 5 LPA', 'No limit'")

    class Config:
        json_schema_extra = {
            "example": {
                "interests": ["machine learning", "data analysis", "mathematics"],
                "skills": ["Python", "Excel"],
                "academic_scores": {"math": 92, "physics": 88, "chemistry": 75},
                "personality_traits": ["analytical", "technical"],
                "current_education": "B.Tech CSE 2nd year",
            }
        }


class CareerPath(BaseModel):
    title: str
    description: str
    match_percentage: float
    required_skills: List[str]
    skills_to_learn: List[str]
    average_salary_lpa: str
    growth_rate: str  # "High" / "Medium" / "Low"
    demand_level: str
    top_companies: List[str]
    recommended_courses: List[str]
    timeline_months: int


class CareerOutput(BaseModel):
    career_paths: List[CareerPath]
    summary: str
    immediate_action: str
    source: str = "ai"  # "ai" or "rule_based" (fallback)
    generated_at: datetime = Field(default_factory=datetime.utcnow)


class CareerResultDB(BaseModel):
    """Stored in MongoDB career_results collection."""
    user_id: str
    input_data: Dict[str, Any]
    result: Dict[str, Any]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_cached: bool = False
