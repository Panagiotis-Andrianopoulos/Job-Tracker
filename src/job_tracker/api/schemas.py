from pydantic import BaseModel, Field

class JobPostingRequest(BaseModel):
    """Request to parse and save a job posting."""
    job_text: str = Field(..., min_length=20, description="Raw text of the job posting")
    job_url: str | None = Field(None, description="Optional URL of the posting")

class JobPostingResponse(BaseModel):
    """Response after parsing a job posting."""
    success: bool
    application_id: int | None = None
    parsed_data: dict | None = None
    error: str | None = None

class SkillMatchRequest(BaseModel):
    """Request to match CV skills against a job."""
    cv_skills: list[str] = Field(..., min_length=1)
    job_id: int = Field(..., description="Application ID to match against")

class SkillMatchResponse(BaseModel):
    """Response with match results."""
    match_percentage: float
    matched_skills: list[dict]
    missing_skills: list[str]

class TailorRequest(BaseModel):
    """Request to tailor CV for a specific job."""
    cv_text: str = Field(..., min_length=50)
    job_id: int = Field(..., description="Application ID to tailor for")

class TailorResponse(BaseModel):
    """Response with tailored CV content."""
    success: bool
    data: dict | None = None
    error: str | None = None

class ApplicationResponse(BaseModel):
    """Single application summary."""
    id: int
    company: str
    role: str
    location: str | None
    status: str
    match_score: float | None
    salary_range: str | None
    created_at: str | None

class StatusUpdateRequest(BaseModel):
    """Request to update application status."""
    status: str = Field(..., pattern="^(saved|applied|interview|rejected|offer|accepted)$")

class HealthResponse(BaseModel):
    status: str
    llm: str
    database: str