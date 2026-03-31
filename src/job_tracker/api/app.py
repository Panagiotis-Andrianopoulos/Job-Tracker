import json
from fastapi import FastAPI, HTTPException
from job_tracker.api.schemas import (
    JobPostingRequest, JobPostingResponse,
    SkillMatchRequest, SkillMatchResponse, 
    TailorRequest, TailorResponse,
    ApplicationResponse, StatusUpdateRequest,
    HealthResponse
)
from job_tracker.parsers.job_parser import parse_job_posting
from job_tracker.matching.skill_matcher import match_skills
from job_tracker.tailoring.cv_tailor import tailor_cv
from job_tracker.tracking.database import (
    init_db, add_application, get_all_applications,
    update_status, update_match_score
)

init_db()

app = FastAPI(
    title="AI Job Application Tracker API",
    description="NLP-powered job tracking: parse postings, match skills, tailor CVs",
    version="1.0.0"
)

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        llm="Groq (llama-3.1-8b-instant)",
        database="SQLite"
    )

@app.post("/jobs/parse", response_model=JobPostingResponse)
async def parse_and_save_job(request: JobPostingRequest):
    """
    Parse a job posting and save it to the database.
    
    Accept raw text of a job posting, uses LLM to extract
    structured data and stores it as a new application.
    """
    result = parse_job_posting(request.job_text)
    
    if not result["success"]:
        return JobPostingResponse(success=False, error=result["error"])
    
    app_id = add_application(
        parsed_job=result["data"],
        job_url=request.job_url,
        job_text=request.job_text
    )

    return JobPostingResponse(
        success=True,
        application_id=app_id,
        parsed_data=result["data"]
    )

@app.get("/jobs", response_model=list[ApplicationResponse])
async def list_applications():
    """Get all tracked applications."""
    apps = get_all_applications()
    return [
        ApplicationResponse(
            id=app["id"],
            company=app["company"],
            role=app["role"],
            location=app["location"],
            status=app["status"],
            match_score=app.get("match_score"),
            salary_range=app.get("salary_range"),
            created_at=app.get("created_at")
        )
        for app in apps
    ]

@app.patch("/jobs/{job_id}/status")
async def change_status(job_id: int, request: StatusUpdateRequest):
    """Update application status (saved/applied/interview/rejected/offer/accepted)."""
    try:
        update_status(job_id, request.status)
        return {"success": True, "job_id": job_id, "new_status": request.status}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/match", response_model=SkillMatchResponse)
async def skill_match(request: SkillMatchRequest):
    """
    Match CV skills against a job posting's requirements.
    
    Uses sentence embeddings + cosine similarity for semantic matching.
    """
    apps = get_all_applications()
    job = next((a for a in apps if a["id"] == request.job_id), None)

    if not job:
        raise HTTPException(status_code=404, detail="Application not found")
    
    job_skills = job.get("required_skills", [])
    if isinstance(job_skills, str):
        job_skills = json.loads(job_skills)

    result = match_skills(request.cv_skills, job_skills)

    update_match_score(request.job_id, result["match_percentage"])

    return SkillMatchResponse(
        match_percentage=result["match_percentage"],
        matched_skills=result["matched_skills"],
        missing_skills=result["missing_skills"]
    )

@app.post("/tailor", response_model=TailorResponse)
async def tailor(request: TailorRequest):
    """
    Generate tailored CV content for a specific job application.
    
    Uses LLM to create customized summary, bullet points
    and cover letter suggestions.
    """
    apps = get_all_applications()
    job = next((a for a in apps if a["id"] == request.job_id), None)

    if not job:
        raise HTTPException(status_code=404, detail="Application not found")
    
    job_text = job.get("job_text", "")
    if not job_text:
        raise HTTPException(status_code=400, detail="No job text stored for this application")
    
    result = tailor_cv(
        cv_text=request.cv_text,
        job_text=job_text
    )

    return TailorResponse(
        success=result["success"],
        data=result.get("data"),
        error=result.get("error")
    )