"""
Pydantic models for College Predictor module.
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from datetime import datetime


class ExamType(str, Enum):
    NEET = "NEET"
    JEE_MAINS = "JEE_MAINS"
    JEE_ADVANCED = "JEE_ADVANCED"
    EAMCET = "EAMCET"
    EAMCET_BIPC = "EAMCET_BIPC"
    KCET = "KCET"
    MHT_CET = "MHT_CET"
    COMEDK = "COMEDK"


class Category(str, Enum):
    GENERAL = "General"
    OBC = "OBC"
    SC = "SC"
    ST = "ST"
    EWS = "EWS"
    PWD = "PWD"


class CollegeType(str, Enum):
    GOVERNMENT = "Government"
    PRIVATE = "Private"
    DEEMED = "Deemed"
    CENTRAL = "Central"


class CollegePredictorInput(BaseModel):
    exam: ExamType
    rank: int = Field(..., gt=0, description="Your rank in the exam")
    category: Category = Category.GENERAL
    state: str = Field(..., description="Home state for quota consideration")
    preferred_states: Optional[List[str]] = Field(
        default=None,
        description="States where you'd like to study"
    )
    max_fees_lpa: Optional[float] = Field(
        default=None,
        description="Maximum annual fees in Lakhs"
    )
    preferred_branch: Optional[str] = Field(
        default=None,
        description="Optional branch or discipline filter (e.g. 'Agriculture', 'Pharmacy')"
    )
    college_type: Optional[List[CollegeType]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "exam": "NEET",
                "rank": 25000,
                "category": "OBC",
                "state": "Andhra Pradesh",
                "preferred_states": ["Andhra Pradesh", "Telangana"],
                "max_fees_lpa": 5.0,
            }
        }


class CutoffEntry(BaseModel):
    year: int
    category: str
    quota: str = "AIQ"
    opening_rank: Optional[int] = None
    closing_rank: int

class CollegeEntry(BaseModel):
    """Represents a single college from the dataset."""
    college_id: str
    name: str
    location: str
    state: str
    exam: str
    branch: str
    college_type: str
    fees_lpa: float
    nirf_rank: Optional[int] = None
    facilities: List[str] = []
    website: Optional[str] = None
    placement_avg_lpa: Optional[float] = None
    established: Optional[int] = None
    cutoffs: List[CutoffEntry] = []

class CollegePrediction(BaseModel):
    """A prediction entry with classification."""
    college: CollegeEntry
    classification: str  # "Safe" | "Target" | "Dream"
    admission_chance_percent: float
    rank_gap: int  # rank minus average cutoff
    avg_cutoff: float

class CollegePredictorOutput(BaseModel):
    safe: List[CollegePrediction]
    target: List[CollegePrediction]
    dream: List[CollegePrediction]
    total_found: int
    query_rank: int
    exam: str
    generated_at: datetime = Field(default_factory=datetime.now)
