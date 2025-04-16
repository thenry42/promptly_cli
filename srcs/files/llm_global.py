from files.config import get_api_key, get_ollama_addr
from .llm_ollama import get_ollama_models
from .llm_openai import get_openai_models
from .llm_deepseek import get_deepseek_models
from .llm_gemini import get_gemini_models
from .llm_mistral import get_mistral_models
from .llm_anthropic import get_anthropic_models


def retrieve_models(provider):
    """Retrieve all models for a given provider"""
    if provider == "ollama":
        return get_ollama_models(get_ollama_addr())
    elif provider == "openai":
        return get_openai_models(get_api_key(provider))
    elif provider == "deepseek":
        return get_deepseek_models(get_api_key(provider))
    elif provider == "gemini":
        return get_gemini_models(get_api_key(provider))
    elif provider == "mistral":
        return get_mistral_models(get_api_key(provider))
    elif provider == "anthropic":
        return get_anthropic_models(get_api_key(provider))
    else:
        pass
