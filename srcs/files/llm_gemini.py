from google import genai


def get_gemini_models(api_key):
    """Get all models from the Gemini API"""
    try:
        client = genai.Client(api_key=api_key)
        models = client.models.list()
        res = [model.name for model in models]
        return res
    except Exception as e:
        return []


def gemini_single_completion(model, prompt, api_key):
    return ""
