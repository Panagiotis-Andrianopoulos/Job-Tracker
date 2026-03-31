import json
from job_tracker.llm.provider import create_llm

CV_PARSER_PROMPT = """You are a CV/resume parser. Extract structured information from the following CV text.

Return ONLY valid JSON with these fields:
{{
    "name": "full name",
    "email": "email if present, otherwise null",
    "location": "location if present, otherwise null",
    "summary": "preofessional summary in 2-3 sentences",
    "skills": ["skill1", "skill2", ...],
    "experience": [
        {{
            "title": "job title",
            "company": "company name",
            "duration": "time period",
            "description": "brief description"
        }}
    ],
    "education": [
        {{
            "degree": "degree name",
            "institution": "university/school",
            "year": "graduation year or period"
        }}
    ],
    "certifications": ["cert1", "cert2", ...],
    "languages": ["language1", "language2", ...]
}}

IMPORTANT: 
- Extract All skills mentioned anywhere in the CV (technical skills, tools, frameworks, languages).
- Return ONLY the JSON, no other text.

CV TEXT:
{cv_text}"""

def parse_cv(cv_text: str) -> dict:
    """
    Extract structured data from free text Cv/resume using an LLM.
    
    Args:
        cv_text: Raw text of a CV/resume.
    Returns:
        Dictionary with 'success' bool and either 'data' (parsed fields)
        or 'error' message.
    """

    llm = create_llm(temperature=0.1)
    prompt = CV_PARSER_PROMPT.format(cv_text=cv_text)
    response = llm.invoke(prompt)

    try:
        content = response.content.strip()
        if content.startswith("```"):
            content = content.split("\n", 1)[1]
            content = content.rsplit("```", 1)[0]

        parsed = json.loads(content)
        return {"success": True, "data": parsed}
    
    except json.JSONDecodeError as e:
        return {"success": False, "error": f"Failed to parse LLM response: {e}", "raw": response.content}