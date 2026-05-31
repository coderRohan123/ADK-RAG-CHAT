import os

from app.services.document_parser import (
    extract_pdf_text,
    extract_excel_text
)

from app.services.embeddings import embed_text
from app.services.vector_store import add_embeddings

from app.config import (
    CHUNK_SIZE,
    CHUNK_OVERLAP
)

# -----------------------------------
# Chunking
# -----------------------------------
def chunk_text(text):

    chunks = []

    start = 0

    while start < len(text):

        end = start + CHUNK_SIZE

        chunk = text[start:end]

        chunks.append(chunk)

        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks

# -----------------------------------
# Ingestion
# -----------------------------------
def ingest_document(file_path, filename):

    ext = os.path.splitext(filename)[1].lower()

    # -----------------------------
    # Extract
    # -----------------------------
    if ext == ".pdf":

        documents = extract_pdf_text(file_path)

    elif ext in [".xlsx", ".xls"]:

        documents = extract_excel_text(file_path)

    else:
        raise Exception("Unsupported file type")

    all_chunks = []
    all_metadata = []

    # -----------------------------
    # Chunk with metadata
    # -----------------------------
    for doc in documents:

        chunks = chunk_text(doc["text"])

        for chunk in chunks:

            metadata = {
                "text": chunk,
                "source": filename
            }

            # Add page if PDF
            if "page" in doc:
                metadata["page"] = doc["page"]

            # Add sheet if Excel
            if "sheet" in doc:
                metadata["sheet"] = doc["sheet"]

            all_chunks.append(chunk)
            all_metadata.append(metadata)

    # -----------------------------
    # Embeddings
    # -----------------------------
    embeddings = embed_text(all_chunks)

    # -----------------------------
    # Store in FAISS
    # -----------------------------
    add_embeddings(
        embeddings=embeddings,
        metadata_list=all_metadata
    )