import openai


def get_openai_models(api_key):
    """Get all models from the OpenAI API"""
    try:
        client = openai.OpenAI(api_key=api_key) 
        models = client.models.list()
        res = [model.id for model in models]
        return res
    except Exception as e:
        return []


