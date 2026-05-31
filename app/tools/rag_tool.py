from google.adk.tools import FunctionTool

from app.services.rag_service import retrieve_context

def search_documents(query: str) -> str:

    results = retrieve_context(query)

    if not results:
        return "No relevant documents found."

    formatted_context = ""

    for i, result in enumerate(results, start=1):

        formatted_context += f"""
DOCUMENT EXCERPT {i}

CONTENT:
{result['text']}

SOURCE:
File: {result['source']}
"""

        # PDF citation
        if "page" in result:
            formatted_context += f"Page: {result['page']}\n"

        # Excel citation
        if "sheet" in result:
            formatted_context += f"Sheet: {result['sheet']}\n"

        formatted_context += "\n-----------------------------\n"

    return formatted_context

rag_tool = FunctionTool(search_documents)