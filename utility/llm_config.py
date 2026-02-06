import os
from dotenv import load_dotenv

load_dotenv()


llm_config={
            "temperature": 0,
            "config_list": [
                {
                    "model": os.getenv("GROQ_MODEL"),
                    "api_key": os.getenv("GROQ_API_KEY"),
                    "base_url": "https://api.groq.com/openai/v1",
                }
            ]
        }