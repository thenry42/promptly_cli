import anthropic


def get_anthropic_models(api_key):
    """Get all models from the Anthropic API"""
    try:
        client = anthropic.Anthropic(api_key=api_key)
        models = client.models.list()
        res = [model.id for model in models]
        return res
    except Exception as e:
        return []
