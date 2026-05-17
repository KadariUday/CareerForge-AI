"""Resume analyzer router — handles PDF upload and analysis."""
import os
import logging
from datetime import datetime
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, BackgroundTasks
from models.resume import ResumeAnalysisRequest, ResumeAnalysisResult, ResumeInDB
from models.user import UserResponse
from services.auth_service import get_current_user
from config.database import get_db
from config.settings import settings
from ai_services import analyze_resume, extract_text_from_pdf

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/resume", tags=["Resume Analyzer"])

ALLOWED_TYPES = {"application/pdf", "text/plain"}
MAX_SIZE = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024


async def _save_resume_record(user_id: str, filename: str, raw_text: str,
                               analysis: dict, job_description: str = None,
                               target_role: str = None, file_path: str = ""):
    """Background task: save resume + analysis to MongoDB."""
    try:
        db = get_db()
        if db:
            doc = ResumeInDB(
                user_id=user_id, filename=filename, file_path=file_path,
                raw_text=raw_text[:5000], analysis=analysis,
                job_description=job_description, target_role=target_role,
            ).model_dump()
            await db.resumes.insert_one(doc)
    except Exception as e:
        logger.error(f"Failed to save resume record: {e}")


@router.post("/analyze", response_model=ResumeAnalysisResult)
async def analyze_resume_endpoint(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="PDF resume file"),
    job_description: str = Form(default=None),
    target_role: str = Form(default=None),
    current_user: UserResponse = Depends(get_current_user),
):
    """
    Upload a PDF resume and receive a comprehensive ATS analysis.
    - Extracts text from PDF
    - Computes ATS score (0-100)
    - Identifies missing keywords
    - Generates AI-powered improvement suggestions
    """
    # Validate file type
    if file.content_type not in ALLOWED_TYPES and not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    # Read file content
    file_content = await file.read()
    if len(file_content) > MAX_SIZE:
        raise HTTPException(status_code=413, detail=f"File too large. Max {settings.MAX_UPLOAD_SIZE_MB}MB.")
    if len(file_content) < 100:
        raise HTTPException(status_code=400, detail="File appears to be empty.")

    result = await analyze_resume(
        file_content=file_content,
        filename=file.filename,
        job_description=job_description,
        target_role=target_role,
        user_id=current_user.id,
    )

    # Save physical file to disk
    upload_path = Path(settings.UPLOAD_DIR)
    os.makedirs(upload_path, exist_ok=True)
    
    # Generate unique filename to avoid collisions
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_filename = f"{current_user.id}_{timestamp}_{file.filename}"
    file_path = str(upload_path / safe_filename)
    
    with open(file_path, "wb") as f:
        f.write(file_content)

    # Save to DB in background
    raw_text = extract_text_from_pdf(file_content)
    background_tasks.add_task(
        _save_resume_record, current_user.id, file.filename,
        raw_text, result.model_dump(), job_description, target_role,
        file_path
    )

    return result


@router.get("/history")
async def get_resume_history(
    limit: int = 10,
    current_user: UserResponse = Depends(get_current_user),
):
    """Get user's past resume analyses."""
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database unavailable")

    cursor = db.resumes.find(
        {"user_id": current_user.id},
        {"filename": 1, "analysis.ats_score": 1, "created_at": 1, "target_role": 1}
    ).sort("created_at", -1).limit(limit)

    results = []
    async for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        results.append(doc)
    return {"history": results, "total": len(results)}
