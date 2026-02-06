import os
import requests
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Config
AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
AZURE_SEARCH_INDEX_NAME = "it-ticket-solutions-index"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Clients
client = genai.Client(api_key=GEMINI_API_KEY)

def embed_text(text: str):
    # Gemini embedding model: gemini-embedding-001
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
    )
    return result.embeddings[0].values

def search_similar_solution(query: str, category: str) -> str:
    embedding = embed_text(query)

    url = f"{AZURE_SEARCH_ENDPOINT}/indexes/{AZURE_SEARCH_INDEX_NAME}/docs/search?api-version=2023-07-01-Preview"

    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_SEARCH_KEY
    }

    payload = {
        "search": "",
        "vectors": [
            {
                "value": embedding,
                "fields": "embedding",
                "k": 3
            }
        ],
        "select": "category,problem,solution",
        "filter": f"category eq '{category}'"
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        return f"Error while searching: {response.text}"

    results = response.json().get("value", [])

    if not results:
        return "No matching solutions found."

    response_text = ""
    for idx, doc in enumerate(results, 1):
        response_text += (
            f"\nResult {idx}:\n"
            f"Category: {doc.get('category')}\n"
            f"Problem: {doc.get('problem')}\n"
            f"Solution: {doc.get('solution')}\n"
        )

    return response_text

if __name__ == "__main__":
    query = "My Outlook crashes every time I open it"
    rag_output = search_similar_solution(query, category="Software Bug")
    print(rag_output)