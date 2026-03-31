# Project Findings

## Architecture
- LLM-based extraction for job parsing and CV parsing
- Sentence embeddings + cosine similarity for skill matching
- LLM generation for CV tailoring
- SQLite for application tracking
- Streamlit multi-page dashboard

## Tech Stack
- LLM: Groq API (Llama 3.1 8B) — fast, free tier
- Embeddings: all-MiniLM-L6-v2 (local, 384 dimensions)
- Database: SQLite (file-based, zero config)
- API: FastAPI
- UI: Streamlit (4 pages: dashboard, add job, skill match, tailor CV)

## AI/ML Techniques Used
| Technique              | Where Used      | Purpose                           |
|------------------------|-----------------|-----------------------------------|
| LLM Structured Extract | Job parser      | Extract JSON from free text       |
| LLM Structured Extract | CV parser       | Extract skills from CV            |
| Sentence Embeddings    | Skill matcher   | Convert skills to vectors         |
| Cosine Similarity      | Skill matcher   | Semantic skill comparison         |
| LLM Generation         | CV tailor       | Create customized CV content      |

## Key Observations
- LLM extraction is format-agnostic (works with any job posting style)
- Semantic matching catches "NLP" ↔ "natural language processing" (0.60 similarity)
- "Python" ↔ "Python programming" scores 0.91 (high accuracy)
- Brand names and acronyms are harder for embeddings (FastAPI ↔ REST API = 0.18)
- Temperature matters: 0.1 for extraction, 0.7 for generation
