import streamlit as st
import sys
from pathlib import Path
from job_tracker.parsers.job_parser import parse_job_posting
from job_tracker.tracking.database import init_db, add_application

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

init_db()

st.title("+ Add New Job Application")

job_text = st.text_area(
    "Paste the job posting text here",
    height=300,
    placeholder="Copy and paste the full job description..."
)

job_url = st.text_input("Job URL (optional)", placeholder="https://...")

if st.button("Parse & Save", type="primary"):
    if not job_text.strip():
        st.error("Please paste a job posting first.")
    else:
        with st.spinner("Parsing job posting with AI..."):
            result = parse_job_posting(job_text)

        if result["success"]:
            data = result["data"]
            st.success("Parsed successfully!")

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Company:** {data.get('company')}")
                st.markdown(f"**Role:** {data.get('role')}")
                st.markdown(f"**Location:** {data.get('location')}")
                st.markdown(f"**Level:** {data.get('experience_level')}")
            with col2:
                st.markdown(f"**Salary:** {data.get('salary_range', 'Not specified')}")
                st.markdown(f"**Summary:** {data.get('summary', 'N/A')}")

            st.markdown("**Required Skills:**")
            for skill in data.get("required_skills", []):
                st.markdown(f"- {skill}")

            app_id = add_application(data, job_url=job_url, job_text=job_text)
            st.success(f"Saved to database (ID: {app_id})")

        else:
            st.error(f"Failed to parse: {result['error']}")