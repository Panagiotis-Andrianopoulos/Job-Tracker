import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = Path("data/applications.db")

def get_connection():
    """Create a connection to the SQLite database."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row

    return conn

def init_db():
    """
    Create the applications table if it doesn't exist.
    
    Schema design:
    - id: auto-incrementing primary key
    - company, role, location: basic info from your job parser
    - status: trackw where you are (applied/interview/rejected/offer)
    - required_skills, nice_to_have: stored as JSON strings
    - match_score: calculated by skill matcher (0-100%)
    - applied_date: when you applied
    - follow_up_date: when to follow up
    - notes: free text for your observations
    - job_url: link to the original posting
    - created_at: auto-set timestamp
    """

    conn = get_connection()
    conn.execute("""
            CREATE TABLE IF NOT EXISTS applications(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT NOT NULL,
                role TEXT NOT NULL,
                location TEXT,
                status TEXT DEFAULT 'saved',
                required_skills TEXT,
                nice_to_have TEXT,
                experience_level TEXT,
                salary_range TEXT,
                summary TEXT,
                match_score REAL,
                applied_date TEXT,
                follow_up_date TEXT,
                notes TEXT,
                job_url TEXT,
                job_text TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
    """)
    conn.commit()
    conn.close()

def add_application(parsed_job: dict, job_url: str = None, job_text: str = None) -> int:
    """
    Add a new application from parsed jobs
    
    Args:
    - parsed_job: dict with fields from job parser
    - job_url: original URL of the job posting
    - job_text: raw text of the job posting (for reference)
    Returns:
    - id of the newly created application
    """

    conn = get_connection()
    cursor = conn.execute("""
            INSERT INTO applications (company, role, location, status, required_skills,
                    nice_to_have, experience_level, salary_range, summary, job_url, job_text)
            VALUES (?, ?, ?, 'saved', ?, ?, ?, ?, ?, ?, ?)
        """, (
            parsed_job.get("company", "Unknown"),
            parsed_job.get("role", "Unknown"),
            parsed_job.get("location"),
            json.dumps(parsed_job.get("required_skills", [])),
            json.dumps(parsed_job.get("nice_to_have", [])),
            parsed_job.get("experience_level"),
            parsed_job.get("salary_range"),
            parsed_job.get("summary"),
            job_url,
            job_text
        )
    )
    conn.commit()
    app_id = cursor.lastrowid
    conn.close()
    return app_id

def get_all_applications() -> list[dict]:
    """
    Get all applications, newest first.
    
    Returns list of dicts wit all fields.
    Skills are deserialized from JSON strings back to lists.
    """

    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM applications ORDER BY created_at DESC"
    ).fetchall()
    conn.close()

    applications = []
    for row in rows:
        app = dict(row)
        if app.get("required_skills"):
            app["required_skills"] = json.loads(app["required_skills"])
        if app.get("nice_to_have"):
            app["nice_to_have"] = json.loads(app["nice_to_have"])
        applications.append(app)

    return applications

def update_status(app_id: int, status: str):
    """
    Update application status
    
    Valid statuses: saved, applied, interview, rejected, offer, accepted
    """

    valid = {"saved", "applied", "interview", "rejected", "offer", "accepted"}
    if status not in valid: 
        raise ValueError(f"Invalid status: {status}. Must be one of {valid}")
    
    conn = get_connection()
    conn.execute("UPDATE applications SET status = ? WHERE id = ?", (status, app_id))
    conn.commit()
    conn.close()

def update_match_score(app_id: int, score: float):
    """Update the skill match score for an application."""
    conn = get_connection()
    conn.execute("UPDATE applications SET match_score = ? WHERE id = ?", (score, app_id))
    conn.commit()
    conn.close()

def delete_application(app_id: int):
    """Delete an application by ID."""
    conn = get_connection()
    conn.execute("DELETE FROM applications WHERE id = ?", (app_id,))
    conn.commit()
    conn.close()