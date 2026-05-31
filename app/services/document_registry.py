import os
import pickle
import hashlib

REGISTRY_PATH = "app/storage/document_registry.pkl"

# Load existing registry
if os.path.exists(REGISTRY_PATH):

    with open(REGISTRY_PATH, "rb") as f:
        registry = pickle.load(f)

else:
    registry = {}

# Generate SHA256 hash
def generate_file_hash(content: bytes):

    sha = hashlib.sha256()

    sha.update(content)

    return sha.hexdigest()

# Check if document already exists
def document_exists(file_hash):

    return file_hash in registry

# Register new document
def register_document(file_hash, filename):

    registry[file_hash] = {
        "filename": filename
    }

    with open(REGISTRY_PATH, "wb") as f:
        pickle.dump(registry, f)