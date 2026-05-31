import os

from fastapi import APIRouter
from fastapi import UploadFile, File
from fastapi import HTTPException

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.schemas.chat import ChatRequest
from app.agents.agent import agent

from app.services.ingestion import ingest_document
from app.config import APP_NAME, UPLOAD_DIR

# NEW IMPORTS
from app.services.document_registry import (
    generate_file_hash,
    document_exists,
    register_document
)

router = APIRouter()

session_service = InMemorySessionService()

runner = Runner(
    agent=agent,
    app_name=APP_NAME,
    session_service=session_service
)

os.makedirs(UPLOAD_DIR, exist_ok=True)

# -----------------------------------
# Upload Endpoint
# -----------------------------------
@router.post("/upload")

async def upload_document(file: UploadFile = File(...)):

    filename = file.filename

    ext = os.path.splitext(filename)[1].lower()

    if ext not in [".pdf", ".xlsx", ".xls"]:

        raise HTTPException(
            status_code=400,
            detail="Only PDF and Excel supported"
        )

    # Read file content
    content = await file.read()

    # Generate file hash
    file_hash = generate_file_hash(content)

    # Check duplicate
    if document_exists(file_hash):

        return {
            "message": "Document already indexed"
        }

    # Save file
    save_path = os.path.join(
        UPLOAD_DIR,
        filename
    )

    with open(save_path, "wb") as f:
        f.write(content)

    # Ingest document
    ingest_document(
        file_path=save_path,
        filename=filename
    )

    # Register document
    register_document(
        file_hash,
        filename
    )

    return {
        "message": "File uploaded and indexed successfully"
    }

# -----------------------------------
# Chat Endpoint
# -----------------------------------
@router.post("/chat")

async def chat(req: ChatRequest):

    try:

        await session_service.create_session(
            app_name=APP_NAME,
            user_id=req.user_id,
            session_id=req.session_id
        )

    except:
        pass

    message = types.Content(
        role="user",
        parts=[types.Part(text=req.query)]
    )

    final_response = ""

    async for event in runner.run_async(
        user_id=req.user_id,
        session_id=req.session_id,
        new_message=message
    ):

        if event.is_final_response():

            if event.content and event.content.parts:

                final_response = event.content.parts[0].text

    return {
        "response": final_response
    }