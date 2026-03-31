import streamlit as st
import sys
import fitz
from pathlib import Path
from job_tracker.matching.skill_matcher import match_skills
from job_tracker.tracking.database import init_db, get_all_applications
from job_tracker.tailoring.cv_tailor import tailor_cv

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

init_db()

st.title("Tailor CV")

input_method = st.radio(
    "How do you want to provide your CV?",
    ["Upload CV (PDF)", "Paste text"],
    horizontal=True
)

cv_text = ""

if input_method == "Upload CV (PDF)":
    if "cv_text" in st.session_state:
        cv_text = st.session_state["cv_text"]
        st.info("Using previously uploaded CV")
        with st.spinner("Preview CV text"):
            st.text(cv_text[:1000] + "..." if len(cv_text) > 1000 else cv_text)
    
    uploaded_file = st.file_uploader("Upload your CV", type=["pdf", "txt"], key="tailor_upload")

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

        st.session_state["cv_text"] = cv_text
        st.success("CV loaded successfully")
else:
    cv_text = st.text_area(
        "Paste your CV text",
        height=200,
        placeholder="Paste your full CV here..."
    )

st.markdown("---")

apps = get_all_applications()
if not apps:
    st.info("No applications yet. Add a job first!")
elif not cv_text.strip():
    st.info("Upload or paste your CV first.")
else:
    job_options = {f"{a['company']} - {a['role']} (ID: {a['id']})": a for a in apps}
    selected = st.selectbox("Select a job to tailor for", list(job_options.keys()))

    if st.button("Generate Tailored Content", type="primary"):
        if not cv_text.strip():
            st.error("Please paste your CV first.")
        else:
            job = job_options[selected]
            job_text = job.get("job_text", "")

            if not job_text:
                st.error("No job text stored for this application.")
            else:
                with st.spinner("AI is tailoring your CV..."):
                    result = tailor_cv(cv_text, job_text)

                if result["success"]:
                    data = result["data"]

                    st.markdown("### Tailored summary")
                    st.info(data.get("tailored_summary", ""))

                    st.markdown("### Tailored Bullet Points")
                    for bullet in data.get("tailored_bullets", []):
                        st.markdown(f"- {bullet}")
                    
                    st.markdown("### Cover Letter Points")
                    for point in data.get("cover_letter_points", []):
                        st.markdown(f"- {point}")

                    st.markdown("### Skills to Highlight")
                    skills = data.get("skills_to_highlight", [])
                    st.markdown(", ".join(skills))

                    st.markdown("### Addressing Gaps")
                    st.warning(data.get("gaps_to_address", ""))
                else:
                    st.error(f"Failed: {result['error']}")

