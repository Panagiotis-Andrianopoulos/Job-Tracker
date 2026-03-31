from job_tracker.matching.embeddings import embed_text, embed_list, cosine_similarity

def match_skills(cv_skills: list[str], job_skills: list[str], threshold: float = 0.5) -> dict:
    """
    Compare CV skills against a job requirements using semantic similarity.
    
    1. Embed all CV skills and all job skills into vectors
    2. For each job skill, find the most similar CV skill
    3. If similarity > threshold, count it as a match
    4. Calculate overall match percentage
    
    threshold=0.5:
    - Above 0.5: sementically related
    - Above 0.7: very similar
    - Below 0.5: probably unrelated
    
    Args:
        cv_skills: List of skills from your CV.
        job_skills: List of required skills from job posting
        threshold: Minimum similarity to count as a match
    
    Return:
        Dictionary with match_percentange, matched_skills, missing_skills
        and detailed similarity scores.
    """

    if not cv_skills or not job_skills:
        return {
            "match_percentage": 0.0,
            "matched_skills": [],
            "missing_skills": job_skills or [],
            "details": []
        }
    
    cv_embeddings = embed_list(cv_skills)
    job_embeddings = embed_list(job_skills)

    matched = []
    missing = []
    details = []

    for i, job_skill in enumerate(job_skills):
        best_score = 0.0
        best_cv_skill = None

        for j, cv_skill in enumerate(cv_skills):
            score = cosine_similarity(job_embeddings[i], cv_embeddings[j])
            if score > best_score:
                best_score = score
                best_cv_skill = cv_skill
        
        detail = {
            "job_skill": job_skill,
            "best_cv_match": best_cv_skill,
            "similarity": round(best_score, 3),
            "is_match": best_score >= threshold
        }
        details.append(detail)

        if best_score >= threshold:
            matched.append(detail)
        else:
            missing.append(job_skill)

    match_percentage = (len(matched) / len(job_skills)) * 100 if job_skills else 0

    return {
        "match_percentage": round(match_percentage, 1),
        "matched_skills": matched,
        "missing_skills": missing,
        "details": details
    }