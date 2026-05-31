from google.adk.agents import Agent
from app.tools.rag_tool import rag_tool
from dotenv import load_dotenv

load_dotenv()

agent = Agent(
    name="helpful_agent",
    model="gemini-2.5-flash-lite",
    description="RAG assistant",

    instruction="""
You are a helpful RAG assistant.

IMPORTANT RULES:

1. ALWAYS use the rag_tool for questions related to uploaded files/documents.

2. If tool results are used, you MUST include citations.

3. NEVER answer from document context without citations.

4. Citation format MUST be exactly:

Source: <filename> | Page: <page>

OR

Source: <filename> | Sheet: <sheet>

5. At the end of every document-based answer, include the source citation.
""",

    tools=[rag_tool]
)