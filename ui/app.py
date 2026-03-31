import streamlit as st

st.set_page_config(
    page_title="AI Job Tracker",
    page_icon="🏢",
    layout="wide"
)

st.title("🏢 AI Job Application Tracker")
st.markdown("*NLP-powered job tracking: parse postings, match skills, tailor CVs")
st.markdown("---")
st.markdown("### Navigate using the sidebar")
st.markdown("""
    - **Dashboard** - Overview of all your applications
    - **Add Job** - Parse and save a new job posting
    - **Skill Match** - Compare your skills against a job
    - **Tailor CV** - Generate customized CV content
""")