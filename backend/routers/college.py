"""College predictor router with database-backed predictions."""
import logging
from typing import Optional, List
from fastapi import APIRouter, Depends, Query, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase

from ..models.college import CollegePredictorInput, CollegePredictorOutput, CollegePrediction, CollegeEntry
from ..models.user import UserResponse
from ..services.auth_service import get_current_user
from ..services.cache_service import cache_get, cache_set, make_cache_key
from ..config.database import get_db

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/college", tags=["College Predictor"])


def _classify(rank: int, cutoff: int) -> tuple[str, float]:
    """Classify a college as Safe/Target/Dream and compute admission chance."""
    diff = cutoff - rank  # positive = you're better than cutoff
    if diff >= 2000:
        return "Safe", min(95.0, 75 + (diff / 200))
    elif diff >= -1000:
        return "Target", max(40.0, 60 - abs(diff) / 100)
    else:
        return "Dream", max(5.0, 35 - abs(diff) / 200)


@router.post("/predict", response_model=CollegePredictorOutput)
async def predict_colleges(
    data: CollegePredictorInput,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Predict colleges based on rank, exam, category, and state."""
    cache_key = make_cache_key("college_v2", data.exam, data.rank, data.category, data.state)
    cached = await cache_get(cache_key)
    if cached:
        return CollegePredictorOutput(**cached)

    if db is None:
        raise HTTPException(status_code=503, detail="Database connection unavailable")

    # Build query
    query = {
        "exam": data.exam.value.upper(),
        "cutoffs.category": data.category.value
    }

    if data.preferred_states:
        query["state"] = {"$in": data.preferred_states}
    
    if data.max_fees_lpa is not None:
        query["fees_lpa"] = {"$lte": data.max_fees_lpa}
        
    if data.college_type:
        query["college_type"] = {"$in": [ct.value for ct in data.college_type]}

    # Fetch from MongoDB
    cursor = db.college_data.find(query)
    colleges = await cursor.to_list(length=1000)

    safe, target, dream = [], [], []

    for c in colleges:
        c.pop("_id", None)
        
        # Filter cutoffs for the user's category
        relevant_cutoffs = [
            cutoff["closing_rank"] for cutoff in c.get("cutoffs", [])
            if cutoff["category"] == data.category.value
        ]
        
        if not relevant_cutoffs:
            continue
            
        # STEP 6 Improvement: Use average of all available years
        avg_cutoff = sum(relevant_cutoffs) / len(relevant_cutoffs)
        gap = data.rank - avg_cutoff
        
        # STEP 3 Logic: Classification
        if gap <= -2000:
            classification = "Safe"
            chance = min(98.0, 85 + abs(gap) / 200)
        elif gap <= 2000:
            classification = "Target"
            chance = max(40.0, 70 - abs(gap) / 100)
        else:
            classification = "Dream"
            chance = max(5.0, 30 - gap / 300)
        
        try:
            college_entry = CollegeEntry(**c)
            pred = CollegePrediction(
                college=college_entry,
                classification=classification,
                admission_chance_percent=round(chance, 1),
                rank_gap=int(gap),
                avg_cutoff=round(avg_cutoff, 1)
            )
            if classification == "Safe":
                safe.append(pred)
            elif classification == "Target":
                target.append(pred)
            else:
                dream.append(pred)
        except Exception as e:
            logger.warning(f"Skipping invalid college entry: {e}")

    # Sort
    safe.sort(key=lambda x: x.admission_chance_percent, reverse=True)
    target.sort(key=lambda x: x.admission_chance_percent, reverse=True)
    dream.sort(key=lambda x: x.admission_chance_percent, reverse=True)

    result = CollegePredictorOutput(
        safe=safe[:15], target=target[:15], dream=dream[:15],
        total_found=len(safe) + len(target) + len(dream),
        query_rank=data.rank, exam=data.exam.value,
    )

    await cache_set(cache_key, result.model_dump(), ttl=3600)
    return result


@router.get("/list")
async def list_colleges(
    exam: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    limit: int = Query(50, le=200),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Browse all colleges with optional filters (public endpoint)."""
    if db is None:
        raise HTTPException(status_code=503, detail="Database connection unavailable")

    query = {}
    if exam:
        query["exam"] = exam.upper()
    if state:
        query["state"] = {"$regex": state, "$options": "i"}

    cursor = db.college_data.find(query).limit(limit)
    colleges = await cursor.to_list(length=limit)
    
    for c in colleges:
        c.pop("_id", None)

    return {"colleges": colleges, "total": len(colleges)}

