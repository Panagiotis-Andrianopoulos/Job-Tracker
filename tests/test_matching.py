from job_tracker.matching.skill_matcher import match_skills
from job_tracker.matching.embeddings import embed_text, cosine_similarity

def test_embed_text_returns_vector():
    """Embedding should return a numpy array."""
    vec = embed_text("Python programming")
    assert vec.shape[0] == 384

def test_cosine_similarity_identical():
    """Identical texts should have similarity close to 1.0."""
    vec = embed_text("machine learning")
    score = cosine_similarity(vec, vec)
    assert score > 0.99

def test_cosine_similarity_related():
    """Related texts should have higher similarity than unrelated."""
    vec_a = embed_text("Python programming")
    vec_b = embed_text("coding in Python")
    vec_c = embed_text("cooking recipes")

    score_related = cosine_similarity(vec_a, vec_b)
    score_unrelated = cosine_similarity(vec_a, vec_c)

    assert score_related > score_unrelated

def test_match_skills_returns_percentage():
    """Skill matcher should return match percentage."""
    result = match_skills(
        cv_skills=["Python", "SQL"],
        job_skills=["Python programming", "database management"]
    )
    assert "match_percentage" in result
    assert 0 <= result["match_percentage"] <= 100

def test_match_skills_empty():
    """Empty skills should return 0% match."""
    result = match_skills([], ["Python"])
    assert result["match_percentage"] == 0.0