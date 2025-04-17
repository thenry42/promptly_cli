import mistralai


def get_mistral_models(api_key):
    """Get all models from the Mistral API"""
    try:
        client = mistralai.Mistral(api_key=api_key)
        models = client.models.list()
        res = [model.id for model in models.data]
        return res
    except Exception as e:
        return []


def mistral_single_completion(model, prompt, api_key):
    return ""
