"""Career guidance router."""
import logging
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from models.career import CareerInput, CareerOutput
from models.user import UserResponse
from services.auth_service import get_current_user
from config.database import get_db
from ai_services import analyze_career

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/career", tags=["Career Guidance"])


async def _save_result_bg(user_id: str, input_data: dict, result: dict):
    """Background task: persist career result to MongoDB."""
    try:
        db = get_db()
        if db:
            await db.career_results.insert_one({
                "user_id": user_id,
                "input_data": input_data,
                "result": result,
                "created_at": datetime.now(timezone.utc),
            })
    except Exception as e:
        logger.error(f"Failed to save career result: {e}")


@router.post("/analyze", response_model=CareerOutput)
async def analyze_career_endpoint(
    career_input: CareerInput,
    background_tasks: BackgroundTasks,
    current_user: UserResponse = Depends(get_current_user),
):
    """
    Analyze student profile and return top career recommendations.
    Results are cached — repeated identical inputs return instantly.
    """
    try:
        result = await analyze_career(career_input, current_user.id)

        # Save to DB in background (non-blocking)
        background_tasks.add_task(
            _save_result_bg, current_user.id,
            career_input.model_dump() if hasattr(career_input, "model_dump") else career_input.dict(),
            result.model_dump() if hasattr(result, "model_dump") else result.dict()
        )
        return result
    except Exception as e:
        logger.error(f"Career analysis error: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Analysis failed. Please try again later."
        )


@router.get("/history")
async def get_career_history(
    limit: int = 10,
    current_user: UserResponse = Depends(get_current_user),
):
    """Fetch the user's past career analysis results."""
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database unavailable")

    cursor = db.career_results.find(
        {"user_id": current_user.id},
        {"result": 1, "created_at": 1, "_id": 1}
    ).sort("created_at", -1).limit(limit)

    results = []
    async for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        results.append(doc)
    return {"history": results, "total": len(results)}
