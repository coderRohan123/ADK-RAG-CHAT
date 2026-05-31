from app.services.embeddings import embed_text
from app.services.vector_store import search

def retrieve_context(query, top_k=3):

    query_embedding = embed_text([query])

    results = search(
        query_embedding=query_embedding,
        top_k=top_k
    )

    return results