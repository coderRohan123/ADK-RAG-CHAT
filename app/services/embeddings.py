from sentence_transformers import SentenceTransformer
import numpy as np
from app.config import EMBED_MODEL

model = SentenceTransformer(EMBED_MODEL)

def embed_text(texts: list[str]) -> np.ndarray:
    embeddings = model.encode(
        texts,
        normalize_embeddings=True
    )
    return np.array(embeddings, dtype="float32")