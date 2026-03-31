import json
from job_tracker.llm.provider import create_llm

JOB_PARSER_PROMPT = """You are a job posting parser. Extract structured information from the following job posting text.

Return ONLY valid JSON with these fields:
{{
    "company": "company name",
    "role": "job title",
    "location": "location or Remote",
    "required_skills": ["skill1", "skill2", ...],
    "nice_to_have_skills": ["skill1", "skill2", ...],
    "experience_level": "junior/mid/senior",
    "salary_range": "salary info if mentioned, otherwise null",
    "summary": "2-3 sentence summary of the role"
}}

IMPORTANT: Return ONLY the JSON, no other text before or after it.

JOB POSTING:
{job_text}"""

def parse_job_posting(job_text: str) -> dict:
    """
    Extract structured data from free-text job posting using an LLM.
    
    temeprature=0.1: For extraction tasks we want accuracy, not creativity. 
    Very low temperature makes the model deterministic and consistent.

    Args:
        job_text: Raw text of a job posting (from URL or copy-paste)
    Returns:
        Dictionary with 'success' bool and either 'data' (parsed fields)
        or 'error' message.
    """
    
    llm = create_llm(temperature=0.1)
    prompt = JOB_PARSER_PROMPT.format(job_text=job_text)
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