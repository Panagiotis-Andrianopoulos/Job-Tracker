from sentence_transformers import SentenceTransformer
import numpy as np

_model = None

def get_embeddings_model():
    """Load the sentence-transformer model (singleton pattern)"""
    global _model

    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")

    return _model

def embed_text(text: str) -> np.ndarray:
    """
    Convert a text string into a vector (embedding)
    
    1. The model tokenizes the text (split into subwords)
    2. Passes through 6 transform layers
    3. Pools the output into a single 384-dimensional vector
    4. Normalizes to unit length
    """

    model = get_embeddings_model()
    embedding = model.encode(text, convert_to_numpy=True)
    return embedding

def embed_list(texts: list[str]) -> np.ndarray:
    """
    Embed multiple texts at once (more efficient than one by one)
    
    The model can process multiple texts in parallel,
    which is much faster than calling embed_text() in a loop.
    """

    model = get_embeddings_model()
    embeddings = model.encode(texts, convert_to_numpy=True)
    return embeddings

def cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    """
    Compute cosine similarity between two vectors.
    
    Formula: cos(θ) = (A · B) / (||A|| * ||B||)
    
    Cosine measures the ANGLE between vectors, not the distance.
    This means it captures semantic similarity regardless if text length.
    
    Returns: float between -1 and 1 (usually 0 to 1 for text).
    1.0 = identical meaning, 0.0 = completely unrelated
    """

    dot_product = np.dot(vec_a, vec_b)
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)

    if norm_a == 0 or norm_b == 0:
        return 0.0
    
    return float(dot_product / (norm_a * norm_b))