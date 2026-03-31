from job_tracker.parsers.job_parser import parse_job_posting

def test_parse_job_posting():
    """Job parser should extract structured data."""
    result = parse_job_posting("""
        ML Engineer at TestCorp, Remote.
        Requirements: Python, TensorFlow, SQL.
        Salary: 40K EUR.
        """)
    assert result["success"] is True
    assert "company" in result["data"]
    assert "required_skills" in result["data"]


def test_parse_empty_text():
    """Empty text should still return a result (not crash)."""
    result = parse_job_posting("This is a very short text about a job.")
    assert "success" in result