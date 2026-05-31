# ADK Chatbot - RAG-Powered AI Assistant

A production-grade **Retrieval-Augmented Generation (RAG)** chatbot powered by Google's Gemini API, built with FastAPI and intelligent document indexing using FAISS.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Project](#running-the-project)
- [API Endpoints](#api-endpoints)
- [Usage Examples](#usage-examples)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [Development](#development)

## 🎯 Overview

ADK Chatbot is an intelligent conversational AI assistant that combines:

- **Retrieval-Augmented Generation (RAG)** for context-aware responses based on your documents
- **Google Gemini 2.5 Flash** model for high-quality, fast responses
- **Document Processing** supporting PDF and Excel files with automatic indexing
- **Vector Embeddings** using Sentence Transformers for semantic search
- **FastAPI** for a modern, async REST API with automatic documentation

This system answers questions about uploaded documents with proper source citations, ensuring transparency and traceability in every response.

Uploaded files are globally indexed into a shared FAISS vector store and stored on disk, so the RAG tool can retrieve context for any session immediately after upload.

## ✨ Features

- 📄 **Multi-Format Document Support** - PDF and Excel (.xlsx, .xls) file ingestion
- 🌐 **Global Document Index** - Uploaded documents are indexed once and used across all RAG queries
- 🔍 **Semantic Search** - FAISS-based vector similarity matching for retrieval
- 🤖 **AI-Powered Responses** - Google Gemini 2.5 Flash for intelligent reasoning
- 📝 **Source Citations** - Responses include document source and page/sheet references when available
- 🚀 **High Performance** - Async operations and in-memory session management
- 📊 **Automatic Deduplication** - Prevents re-indexing of duplicate documents
- 🔄 **Conversation Memory** - Stores session-based chat history using `InMemorySessionService`
- 📚 **Interactive API Docs** - Swagger UI and ReDoc for easy exploration

## 🏗️ Architecture

```
┌─────────────┐
│   FastAPI   │
│  Server     │
└──────┬──────┘
       │
       ├─→ Upload Handler → Document Parser → FAISS Indexing
       │
       ├─→ Chat Handler → Google ADK Agent → Gemini 2.5 Flash
       │         ↑
       │         └─ RAG Tool (semantic search)
       │
       └─→ Session Manager (in-memory)

Storage:
├── FAISS Index (embeddings)
├── Uploaded Files (PDF/Excel)
└── Document Registry (deduplication)
```

## 📦 Prerequisites

- **Python** 3.13 or higher
- **pip** or **uv** package manager
- **Google API Key** with Generative AI access
- **Git** (for version control)

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd adkchatbot
```

### Step 2: Create Virtual Environment

**Using Python venv:**
```bash
python -m venv .venv

# Activate on Windows
.\.venv\Scripts\Activate.ps1

# Activate on macOS/Linux
source .venv/bin/activate
```

**Using uv (faster):**
```bash
uv init
uv add venv
.venv\Scripts\activate
```

### Step 3: Install Dependencies

**Option A - Using pyproject.toml (Recommended):**
```bash
pip install -e .
```

**Option B - Using requirements.txt:**
```bash
pip install -r requirements.txt
```

**Option C - Using uv:**
```bash
uv sync
```

### Step 4: Set Up Environment Variables

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_api_key_here
```

**How to get your Google API Key:**
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the key and paste it in `.env`

## ⚙️ Configuration

Edit `app/config.py` to customize settings:

```python
# Document storage
UPLOAD_DIR = "app/storage/uploads"
FAISS_DIR = "app/storage/faiss_index"

# Embedding model (all-MiniLM is fast and accurate for most use cases)
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Document chunking for better retrieval
CHUNK_SIZE = 500          # Characters per chunk
CHUNK_OVERLAP = 50        # Overlap for context continuity
```

**Model Options:**
- `gemini-2.5-flash-lite` - Fastest, most cost-effective (default)
- `gemini-2.5-flash` - Balanced speed and quality
- `gemini-2.0-pro` - Highest quality, slower, more expensive

## 🏃 Running the Project

### Quick Start

**On Windows:**
```powershell
python run.py
```

**On macOS/Linux:**
```bash
chmod +x run.sh
./run.sh
```

**Manual Run:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The application will start on:
- **API Server:** http://localhost:8000
- **Interactive Docs (Swagger UI):** http://localhost:8000/docs
- **Alternative Docs (ReDoc):** http://localhost:8000/redoc

## 📡 API Endpoints

### 1. **Upload Document**

```http
POST /upload
Content-Type: multipart/form-data

file: <PDF or Excel file>
```

**Response:**
```json
{
  "message": "File uploaded and indexed successfully"
}
```

**Supported Formats:**
- PDF files (`.pdf`)
- Excel files (`.xlsx`, `.xls`)

**File Validation:**
- Maximum size: No server-side limit (depends on your infrastructure)
- Duplicate Detection: Automatically prevents re-indexing
- Automatic parsing and chunking for optimal retrieval

---

### 2. **Chat with Assistant**

```http
POST /chat
Content-Type: application/json

{
  "user_id": "rohan",
  "session_id": "session2",
  "query": "What is my annual turnover in q1?"
}
```

**Response:**
```json
{
  "response": "AI-generated answer with document-backed context"
}
```

**Notes:**
- `user_id` and `session_id` are used to create and track an in-memory session.
- `query` is sent to the agent, which uses the globally indexed documents for RAG context.
- Uploaded documents are available to all sessions via the shared FAISS index.

---

## 💬 Usage Examples

### Example 1: Upload and Query a Document

**Step 1: Upload a PDF**
```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@financial_report.pdf"
```

**Step 2: Ask a Question**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id": "rohan", "session_id": "session2", "query": "What was the revenue in Q3?"}'
```

**Response:**
```json
{
  "response": "The revenue in Q3 was $2.5 million. Source: financial_report.pdf | Page: 12"
}
```

### Example 2: Using Interactive Swagger UI

1. Navigate to http://localhost:8000/docs
2. Click on **POST /upload** → Click "Try it out"
3. Select a PDF or Excel file and upload
4. Click on **POST /chat** → Click "Try it out"
5. Enter your question in the `message` field
6. Click "Execute"

### Example 3: Using Python Client

```python
import requests

BASE_URL = "http://localhost:8000"

# Upload file
with open("sample.pdf", "rb") as f:
    files = {"file": f}
    response = requests.post(f"{BASE_URL}/upload", files=files)
    print(response.json())

# Ask question
payload = {
    "user_id": "rohan",
    "session_id": "session2",
    "query": "Summarize the main points"
}
response = requests.post(f"{BASE_URL}/chat", json=payload)
print(response.json())
```

---

## 📁 Project Structure

Uploaded documents are stored in `app/storage/uploads`, and the shared vector index is stored in `app/storage/faiss_index`.

```
adkchatbot/
├── app/
│   ├── main.py                    # FastAPI application entry point
│   ├── config.py                  # Configuration settings
│   ├── agents/
│   │   └── agent.py              # Gemini agent with RAG tool
│   ├── api/
│   │   └── routes.py             # REST API endpoints
│   ├── schemas/
│   │   └── chat.py               # Request/response schemas
│   ├── services/
│   │   ├── document_parser.py    # PDF/Excel parsing
│   │   ├── document_registry.py  # Duplicate detection
│   │   ├── embeddings.py         # Embedding generation
│   │   ├── ingestion.py          # Document processing pipeline
│   │   ├── rag_service.py        # RAG logic and retrieval
│   │   └── vector_store.py       # FAISS index management
│   ├── tools/
│   │   └── rag_tool.py           # RAG tool for agent
│   └── storage/
│       ├── uploads/              # Uploaded documents
│       └── faiss_index/          # Vector index
├── run.py                         # Quick start script
├── run.sh                         # Bash startup script
├── pyproject.toml                # Project dependencies
├── requirements.txt              # Alternative dependency file
├── .env                          # Environment variables
└── README.md                     # This file
```

---

## 🔧 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'google.adk'"

**Solution:** Ensure dependencies are installed:
```bash
pip install -e .
```

### Issue: "GOOGLE_API_KEY not found"

**Solution:** Create `.env` file in root directory with your API key:
```env
GOOGLE_API_KEY=your_key_here
```

### Issue: FAISS Index Not Found

**Solution:** The index is created automatically on first document upload. If needed, reset:
```bash
rm -rf app/storage/faiss_index
```

### Issue: "Only PDF and Excel supported" Error

**Solution:** Ensure you're uploading `.pdf`, `.xlsx`, or `.xls` files. Other formats are not supported.

### Issue: Out of Memory with Large Files

**Solution:** Adjust `CHUNK_SIZE` and `CHUNK_OVERLAP` in `config.py` to smaller values:
```python
CHUNK_SIZE = 300
CHUNK_OVERLAP = 25
```

### Issue: Slow Responses

**Solution:** Use the faster model:
```python
model="gemini-2.5-flash-lite"  # in app/agents/agent.py
```

---

## 👨‍💻 Development

### Adding Custom Tools

Edit `app/agents/agent.py` to add new tools to the agent:

```python
from app.tools.custom_tool import custom_tool

agent = Agent(
    name="helpful_agent",
    model="gemini-2.5-flash-lite",
    description="RAG assistant with custom tools",
    tools=[rag_tool, custom_tool]  # Add here
)
```

### Modifying Document Parsing

Update `app/services/document_parser.py` to support additional formats.

### Customizing RAG Behavior

Adjust RAG parameters in `app/services/rag_service.py`:
- Number of retrieved chunks
- Similarity threshold
- Reranking strategy

### Running Tests

```bash
pytest tests/
```

---

## 📝 License

This project is provided as-is for internal use.

## 🤝 Support

For issues, bugs, or feature requests, please contact the development team or open an issue in the repository.

---

## 🚀 Deployment

### Docker

```bash
docker build -t adkchatbot .
docker run -p 8000:8000 -e GOOGLE_API_KEY=your_key adkchatbot
```

### Cloud Deployment

This application can be deployed to:
- **Google Cloud Run** (recommended for Gemini API)
- **Azure Container Instances**
- **AWS ECS/Fargate**
- **Heroku**

---

**Happy Chatting!** 🎉
