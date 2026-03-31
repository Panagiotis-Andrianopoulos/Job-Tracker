import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

def create_llm(model: str = "llama-3.1-8b-instant", temperature: float = 0.3):
    """Create connection with Groq API and return the LLM instance."""

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found. Add it to your .env file.")
    
    llm = ChatGroq(
        model=model,
        temperature=temperature,
        api_key=api_key
    )
    return llm