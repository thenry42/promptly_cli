import ollama
import mistralai
from google import genai
import os
import logging
from dotenv import load_dotenv

load_dotenv("../../.env")

def get_providers() -> list[str]:
    """Get a list of available AI providers based on valid API credentials."""
    providers = []

    try: 
        if ollama.Client():
            providers.append("ollama")  # Green color
    except Exception as e:
        pass
    try:
        if mistralai.Mistral(api_key=os.getenv("MISTRAL_API_KEY")):
            providers.append("mistral")  # Green color
    except Exception as e:
        pass
    try:
        if genai.Client(api_key=os.getenv("GEMINI_API_KEY")):
            providers.append("gemini")  # Green color
    except Exception as e:
        pass

    return providers