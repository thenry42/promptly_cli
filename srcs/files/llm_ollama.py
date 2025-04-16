import ollama


def get_ollama_models(addr):
    """Get all models from the Ollama server"""
    try:
        client = ollama.Client(host=addr)
        models = client.list()
        res = [model["model"] for model in models["models"]]
        return res
    except Exception as e:
        return e