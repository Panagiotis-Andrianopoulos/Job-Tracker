import streamlit as st
import sys
import fitz
from pathlib import Path
from job_tracker.tracking.database import init_db, get_all_applications, update_match_score
from job_tracker.matching.skill_matcher import match_skills
from job_tracker.parsers.cv_parser import parse_cv

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

init_db()

st.title("Skill Match Score")

st.markdown("### Your skills")
input_method = st.radio(
    "How do you want to provide your skills?",
    ["Upload CV (PDF)", "Type manually"],
    horizontal=True
)
cv_skills = []

if input_method == "Upload CV (PDF)":
    uploaded_file = st.file_uploader("Upload your CV", type=["pdf", "txt"])
    if uploaded_file is not None:
        if uploaded_file.name.endswith(".pdf"):
            pdf_bytes = uploaded_file.read()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            cv_text = ""
            for page in doc:
                cv_text += page.get_text()
            doc.close()
        else:
            cv_text = uploaded_file.read().decode("utf-8")
        
        if cv_text.strip():
            with st.spinner("Extracting skills from CV with AI..."):
                result = parse_cv(cv_text)
            
            if result["success"]:
                extracted_skills = result["data"].get("skills", [])
                cv_skills = extracted_skills

                st.success(f"Extracted {len(cv_skills)} skills from CV")
                st.markdown("**Detected skills:**")
                st.markdown(", ".join(cv_skills))

                st.session_state["cv_skills"] = cv_skills
                st.session_state["cv_text"] = cv_text
            else:
                st.error(f"Failed to parse CV: {result['error']}")
            
        else:
            st.warning("Could not extract text from the file.")
    
    elif "cv_skills" in st.session_state:
        cv_skills = st.session_state["cv_skills"]
        st.info(f"Using previously extracted skills ({len(cv_skills)} skills)")
else: 
    cv_skills_text = st.text_area(
        "Enter your skills (one per line)",
        placeholder="Python\nPyTorch\nNLP\nDocker\n...",
        height=150
    )
    if cv_skills_text.strip():
        cv_skills = [s.strip() for s in cv_skills_text.strip().split("\n") if s.strip()]

st.markdown("---")
st.markdown("### Match against a Job")

apps = get_all_applications()
if not apps:
    st.info("No applications yet. Add a job first!")
elif not cv_skills:
    st.info("Upload your CV or type your skills above first.")
else:
    job_options = {f"{a['company']} - {a['role']} (ID: {a['id']})": a for a in apps}
    selected = st.selectbox("Select a job to match against", list(job_options.keys()))

    if st.button("Match Skills", type="primary"):
        job = job_options[selected]
        job_skills = job.get("required_skills", [])
            
        with st.spinner("Calculating skill match score..."):
            result = match_skills(cv_skills, job_skills)

        update_match_score(job["id"], result["match_percentage"])

        st.markdown(f"## Match: {result['match_percentage']:.0f}%")
        st.progress(result["match_percentage"] / 100)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Matched skills")
            for match in result["matched_skills"]:
                st.markdown(
                    f"- **{match['job_skill']}** -> {match['best_cv_match']} "
                    f"({match['similarity']:.0%})"
                )
            
        with col2:
            st.markdown("### Missing Skills")
            for skill in result["missing_skills"]:
                st.markdown(f" - {skill}")