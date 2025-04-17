from files.config import get_api_key, get_ollama_addr
from .llm_ollama import get_ollama_models, ollama_single_completion, ollama_chat_completion
from .llm_openai import get_openai_models, openai_single_completion, openai_chat_completion
from .llm_deepseek import get_deepseek_models, deepseek_single_completion, deepseek_chat_completion
from .llm_gemini import get_gemini_models, gemini_single_completion, gemini_chat_completion
from .llm_mistral import get_mistral_models, mistral_single_completion, mistral_chat_completion
from .llm_anthropic import get_anthropic_models, anthropic_single_completion, anthropic_chat_completion


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

def single_completion(provider, model, prompt):
    """Send a single request to the model"""
    if provider == "ollama":
        return ollama_single_completion(model, prompt)
    elif provider == "openai":
        return openai_single_completion(model, prompt, get_api_key(provider))
    elif provider == "deepseek":
        return deepseek_single_completion(model, prompt, get_api_key(provider))
    elif provider == "gemini":
        return gemini_single_completion(model, prompt, get_api_key(provider))
    elif provider == "mistral":
        return mistral_single_completion(model, prompt, get_api_key(provider))
    elif provider == "anthropic":
        return anthropic_single_completion(model, prompt, get_api_key(provider))
    else:
        pass


def chat_completion(provider, model, prompt, messages):
    """Send a chat request to the model"""
    if provider == "ollama":
        return ollama_chat_completion(model, prompt, messages)
    elif provider == "openai":
        return openai_chat_completion(model, prompt, messages, get_api_key(provider))
    elif provider == "deepseek":
        return deepseek_chat_completion(model, prompt, messages, get_api_key(provider))
    elif provider == "gemini":
        return gemini_chat_completion(model, prompt, messages, get_api_key(provider))
    elif provider == "mistral":
        return mistral_chat_completion(model, prompt, messages, get_api_key(provider))
    elif provider == "anthropic":
        return anthropic_chat_completion(model, prompt, messages, get_api_key(provider))
    else:
        pass