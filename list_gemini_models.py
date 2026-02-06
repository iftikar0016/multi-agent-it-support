import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

try:
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    # List models to see valid names
    pager = client.models.list()
    print("Available models:")
    for model in pager:
        print(f" - {model.name}")
except Exception as e:
    print(f"Error listing models: {e}")
