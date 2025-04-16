from rich.console import Console


def run_no_args():
    console = Console()

    # The user will be prompted to select a model and provider

    # 1. check for all AVAILABLE providers

    # 2. check for all AVAILABLE models

    # 3. select a provider

    # 4. select a model

    # 5. launch the chat in a loop (handle signals EOF, SIGINT, SIGTERM)


def run_with_model(arg):
    console = Console()

    # 1. parse the argument to get the provider and model

    # 2. check if the provider and model are available

    # 3. launch the chat in a loop (handle signals EOF, SIGINT, SIGTERM)


def run_with_model_and_prompt(arg1, arg2):
    console = Console()

    # 1. parse the argument to get the provider and model

    # 2. check if the provider and model are available

    # 3. Send a single request to the model

    # 4. print the response in stream mode
