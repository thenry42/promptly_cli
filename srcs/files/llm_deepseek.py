import openai

BASE_URL = "https://api.deepseek.com"

def get_deepseek_models(api_key):
    """Get all models from the DeepSeek API"""
    try:
        client = openai.OpenAI(api_key=api_key, base_url=BASE_URL)
        models = client.models.list()
        res = [model.id for model in models]
        return res
    except Exception as e:
        return []
