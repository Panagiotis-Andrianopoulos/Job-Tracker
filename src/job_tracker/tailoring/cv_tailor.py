from job_tracker.llm.provider import create_llm
import json

CV_TAILOR_PROMPT = """You are a professional CV/resume writer.

Given a candidate's CV and a job description, create tailored content
that highlights the candidate's most relevant experience and skills
for THIS specific role.

CANDIDATE CV:
{cv_text}

JOB DESCRIPTION:
{job_text}

SKILL MATCH INFO:
Match percentage: {match_pct}%
Matched skills: {matched}
Missing skills: {missing}

Generate the following in JSON format:
{{
    "tailored_summary": "A 3-4 sentence professional summary highlighting the candidate's most relevant experience for this role",
    "tailored_bullets": [
        "Achivement-focused bullet point emphasizing relevant skill 1",
        "Achivement-focused bullet point emphasizing relevant skill 2",
        "Achivement-focused bullet point emphasizing relevant skill 3",
        "Achivement-focused bullet point emphasizing relevant skill 4",
        "Achivement-focused bullet point emphasizing relevant skill 5"
    ],
    "cover_letter_points": [
        "Key point to mention in cover letter 1",
        "Key point to mention in cover letter 2",
        "Key point to mention in cover letter 3"
    ],
    "skills_to_highlight": ["skill1", "skill2", "skill3"],
    "gaps_to_address": "Brief advice on how to address missing skills in the application"
}}

IMPORTANT:
- Focus on what the candidate HAS that matched the job, not what they lack.
- Use strong action verbs (developed, implemented, designed, optimized).
- Be specific and quantify where possible.
- Return ONLY valid JSON, no other text."""

def tailor_cv(cv_text: str, job_text: str, match_result: dict = None) -> dict:
    """
    Generate tailored CV content for a specific job application.
    
    A generic CV gets lost in the pile. A tailored CV that mirrors
    the job's description language and highlights relevant experience
    dramatically improves response rates.
    
    1. Takes the full CV text and job description as context
    2. Optionally takes skill match results for more targeted output
    3. LLM generates customized summary, bullet points and advice
    4. Uses higher temperature (0.7) for creative and engaging writing
    
    Args:
        cv_text: Full text of the candidate's CV.
        job_text: Full text of the job posting.
        match_result: Optional output from skill_matcher for content.
    
    Returns:
        Dictionary with 'success' and either 'data' (tailored content)
        or 'error' message.
    """

    match_pct = "N/A"
    matched = "N/A"
    missing = "N/A"

    if match_result:
        match_pct = match_result.get("match_percentage", "N/A")
        matched = ", ".join(m["job_skill"] for m in match_result.get("matched_skills", []))
        missing = ", ".join(match_result.get("missing_skills", []))

    llm = create_llm(temperature=0.7)

    prompt = CV_TAILOR_PROMPT.format(
        cv_text=cv_text,
        job_text=job_text,
        match_pct=match_pct,
        matched=matched,
        missing=missing
    )

    response = llm.invoke(prompt)

    try:
        content = response.content.strip()
        if content.startswith("```"):
            content = content.split("\n", 1)[1]
            content = content.rsplit("```", 1)[0]

        parsed = json.loads(content)
        return {"success": True, "data": parsed}
    
    except json.JSONDecodeError as e:
        return {"success": False, "error": f"Failed to parse response: {e}", "raw": response.content}