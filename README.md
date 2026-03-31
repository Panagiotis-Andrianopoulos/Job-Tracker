# 🎯 AI Job Application Tracker

> NLP-powered tool that parses job postings, matches your skills, and tailors your CV — built because I needed it myself.

## Highlights

- **Job Parsing** — Paste any job posting, AI extracts company, role, skills, salary
- **Skill Matching** — Upload your CV, get semantic match % against any job using embeddings
- **CV Tailoring** — AI generates customized summary and bullet points per job
- **Application Tracking** — Dashboard to manage status, follow-ups, and analytics
- **100% Practical** — I use this daily for my own job search

## Tech Stack

- **LLM:** Groq API (Llama 3.1 8B) — fast, free
- **Embeddings:** sentence-transformers (all-MiniLM-L6-v2, local)
- **Database:** SQLite
- **API:** FastAPI
- **UI:** Streamlit (multi-page dashboard)
- **Containerization:** Docker

## Quick Start

### Prerequisites
- Python 3.12
- Groq API key (free at [console.groq.com](https://console.groq.com))

### Installation
```bash
git clone https://github.com/YOUR_USERNAME/job-tracker.git
cd job-tracker
uv sync
echo "GROQ_API_KEY=your_key_here" > .env
```

### Launch the dashboard
```bash
streamlit run ui/app.py
```

### Start the API
```bash
uvicorn job_tracker.api.app:app --host 0.0.0.0 --port 8000
```

Visit http://localhost:8000/docs for API documentation.

### Docker
```bash
docker-compose up
```

## Features

###  Dashboard
Track all applications with status management and match scores.

###  Add Job
Paste any job posting — AI extracts structured data automatically.

###  Skill Match
Upload your CV (PDF) or type skills — get semantic match % against any job.

###  Tailor CV
AI generates customized summary, bullet points, and cover letter suggestions.

## AI/ML Techniques

- **LLM Structured Extraction** — Parse unstructured text into JSON
- **Sentence Embeddings** — Convert skills to 384-dim vectors
- **Cosine Similarity** — Semantic skill matching (not just keyword matching)
- **LLM Generation** — Context-aware CV customization

## Project Structure
```
job-tracker/
├── src/job_tracker/
│   ├── parsers/        # Job and CV parsing (LLM extraction)
│   ├── matching/       # Embeddings + cosine similarity
│   ├── tailoring/      # LLM-based CV customization
│   ├── tracking/       # SQLite database + CRUD
│   ├── llm/            # Groq API provider
│   └── api/            # FastAPI application
├── ui/                 # Streamlit dashboard (4 pages)
├── tests/              # Automated tests
├── docs/               # Documentation
├── Dockerfile
└── docker-compose.yml
```