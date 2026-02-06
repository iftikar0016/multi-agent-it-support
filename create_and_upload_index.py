
import os
import json
from tqdm import tqdm
from google import genai
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchField,
    SearchFieldDataType,
    SimpleField,
    SearchableField,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile
)
from azure.search.documents import SearchClient
from dotenv import load_dotenv

load_dotenv()

# ---------------- CONFIG ----------------
AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")  # e.g., https://your-search.search.windows.net
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
AZURE_SEARCH_INDEX_NAME = "it-ticket-solutions-index"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

DATA_FILE = "data/knowledge_base.json"
VECTOR_DIMENSIONS = 768  # Gemini text-embedding-004
# ----------------------------------------

# ---------- Clients ----------
credential = AzureKeyCredential(AZURE_SEARCH_KEY)
index_client = SearchIndexClient(endpoint=AZURE_SEARCH_ENDPOINT, credential=credential)
search_client = SearchClient(endpoint=AZURE_SEARCH_ENDPOINT, index_name=AZURE_SEARCH_INDEX_NAME, credential=credential)


# ---------- Index Creation ----------
def create_index():
    print("📦 Creating index...")

    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True, filterable=True, sortable=True, facetable=True),
        SearchableField(name="category", type=SearchFieldDataType.String, filterable=True, sortable=True, facetable=True),
        SearchableField(name="problem", type=SearchFieldDataType.String, filterable=True, sortable=True, facetable=True),
        SearchableField(name="solution", type=SearchFieldDataType.String, filterable=True, sortable=True, facetable=True),
        SearchField(
            name="embedding",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=VECTOR_DIMENSIONS,
            vector_search_profile_name="default"
        )
    ]

    vector_search = VectorSearch(
        algorithms=[HnswAlgorithmConfiguration(name="default")],
        profiles=[VectorSearchProfile(name="default", algorithm_configuration_name="default")]
    )

    index = SearchIndex(name=AZURE_SEARCH_INDEX_NAME, fields=fields, vector_search=vector_search)

    try:
        # Delete the index if it exists to ensure schema update (e.g. vector dimensions)
        print(f"⚠️ Deleting existing index '{AZURE_SEARCH_INDEX_NAME}' to apply new schema...")
        index_client.delete_index(AZURE_SEARCH_INDEX_NAME)
    except Exception:
        pass  # Index didn't exist, which is fine

    try:
        index_client.create_index(index)
        print(f"✅ Index '{AZURE_SEARCH_INDEX_NAME}' created successfully.")
    except Exception as e:
        print(f"❌ Error creating index: {e}")


# ---------- Embedding ----------
def embed_text(text: str):
    # Gemini embedding model: gemini-embedding-001
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
    )
    return result.embeddings[0].values


# ---------- Upload ----------
def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def upload_documents(docs):
    print(f"\n📤 Uploading {len(docs)} documents...")
    batch_size = 10
    for i in tqdm(range(0, len(docs), batch_size)):
        chunk = docs[i:i+batch_size]
        search_client.upload_documents(documents=chunk)
    print("✅ Upload completed.")

# ---------- Main ----------
def main():
    create_index()

    raw_docs = load_data()
    enriched_docs = []

    print("🔍 Generating embeddings...")
    for doc in tqdm(raw_docs):
        embedding = embed_text(doc["problem"])
        doc["embedding"] = embedding
        enriched_docs.append(doc)

    upload_documents(enriched_docs)


if __name__ == "__main__":
    main()