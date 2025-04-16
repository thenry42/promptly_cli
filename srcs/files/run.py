from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.table import Table
from rich.style import Style
from rich.markdown import Markdown
from rich.status import Status
from .config import get_available_providers
from .llm_global import retrieve_models
from .chat import chat
from .completion import single_completion

def run_no_args():
    console = Console()

    # 1. check for all AVAILABLE providers
    providers = ["openai", "mistral", "anthropic", "deepseek", "gemini", "ollama"]
    available_providers = []
    
    with Status("[bold green]Loading available providers...", spinner="dots") as status:
        # Create a nice table for providers
        provider_table = Table(show_header=True, header_style="bold green")
        provider_table.add_column("#", style="dim", width=4)
        provider_table.add_column("Provider", style="green")
        provider_table.add_column("Available Models", style="cyan", justify="right")
        
        for i, provider in enumerate(providers, start=1):
            status.update(f"[bold green]Checking provider: [cyan]{provider}[/cyan]...")
            models = retrieve_models(provider)
            if models != []:
                provider_table.add_row(
                    str(i), 
                    provider, 
                    f"{len(models)} models"
                )
                available_providers.append(provider)
    
    console.print("")
    console.print(provider_table)
    console.print("")

    while True:
        try:
            prompt = Prompt.ask(
                "[bold green]Select a provider[/bold green]", 
                default="1",
                show_default=True,
                console=console
            )
            try:
                provider_idx = int(prompt) - 1
                if 0 <= provider_idx < len(available_providers):
                    provider = available_providers[provider_idx]
                    console.print(f"[bold green]Selected provider:[/bold green] [bold cyan]{provider}[/bold cyan]")
                    break
                else:
                    console.print()
                    console.print(Panel(
                        f"Please enter a number between 1 and {len(available_providers)}", 
                        title="Invalid Selection",
                        border_style="red",
                        expand=False
                    ))
                    console.print()
            except ValueError:
                console.print(Panel("Please enter a valid number", title="Error", border_style="red", expand=False))
        except (KeyboardInterrupt, EOFError):
            console.print("\n", Panel("Interrupted. Please select a provider to continue.", border_style="yellow", expand=False))

    # 2. check for all AVAILABLE models
    with Status(f"[bold green]Loading models for [cyan]{provider}[/cyan]...", spinner="dots") as status:
        models = retrieve_models(provider)
        
        # Create a nice table for models
        model_table = Table(show_header=True, header_style="bold green")
        model_table.add_column("#", style="dim", width=4)
        model_table.add_column("Model", style="green")
        
        for i, model in enumerate(models, start=1):
            model_table.add_row(str(i), model)
    
    console.print("")
    console.print(model_table)
    console.print("")

    while True:
        try:
            prompt = Prompt.ask(
                "[bold green]Select a model[/bold green]",
                default="1",
                show_default=True,
                console=console
            )
            try:
                model_idx = int(prompt) - 1
                if 0 <= model_idx < len(models):
                    model = models[model_idx]
                    console.print(f"[bold green]Selected model:[/bold green] [bold cyan]{model}[/bold cyan]")
                    break
                else:
                    console.print()
                    console.print(Panel(
                        f"Please enter a number between 1 and {len(models)}", 
                        title="Invalid Selection",
                        border_style="red",
                        expand=False
                    ))
                    console.print()
            except ValueError:
                console.print(Panel("Please enter a valid number", title="Error", border_style="red", expand=False))
        except (KeyboardInterrupt, EOFError):
            console.print("\n", Panel("Interrupted. Please select a model to continue.", border_style="yellow", expand=False))

    # Show startup message
    console.print("")
    console.print(Panel(
        f"[bold]Starting chat with [green]{provider}[/green]/[cyan]{model}[/cyan][/bold]",
        border_style="green",
        expand=False
    ))
    
    # 3. launch the chat in a loop (handle signals EOF, SIGINT, SIGTERM)
    chat(provider, model)

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
