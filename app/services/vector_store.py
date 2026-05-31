import faiss
import os
import pickle

from app.config import FAISS_DIR

INDEX_PATH = f"{FAISS_DIR}/index.faiss"
METADATA_PATH = f"{FAISS_DIR}/metadata.pkl"

os.makedirs(FAISS_DIR, exist_ok=True)

dimension = 384

# -----------------------------
# Load Existing
# -----------------------------
if os.path.exists(INDEX_PATH):

    index = faiss.read_index(INDEX_PATH)

    with open(METADATA_PATH, "rb") as f:
        metadata_store = pickle.load(f)

else:

    index = faiss.IndexFlatIP(dimension)

    metadata_store = []

# -----------------------------
# Save
# -----------------------------
def save_index():

    faiss.write_index(index, INDEX_PATH)

    with open(METADATA_PATH, "wb") as f:
        pickle.dump(metadata_store, f)

# -----------------------------
# Add
# -----------------------------
def add_embeddings(
    embeddings,
    metadata_list
):

    global metadata_store

    index.add(embeddings)

    metadata_store.extend(metadata_list)

    save_index()

# -----------------------------
# Search
# -----------------------------
def search(
    query_embedding,
    top_k=5
):

    scores, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for idx in indices[0]:

        if idx == -1:
            continue

        results.append(metadata_store[idx])

    return results