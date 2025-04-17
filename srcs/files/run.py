from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.style import Style
from rich.markdown import Markdown
from rich.status import Status
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style as PromptStyle
import os
from .config import get_available_providers
from .llm_global import retrieve_models, single_completion
from .chat import chat


def run_no_args():
    console = Console()
    
    # Set up prompt_toolkit session with history
    history_file = os.path.join(os.path.expanduser("~"), ".promptly_history")
    session = PromptSession(
        history=FileHistory(history_file),
        auto_suggest=AutoSuggestFromHistory(),
        enable_history_search=True,
        complete_in_thread=True,
        complete_while_typing=True
    )
    
    # Define prompt style - corrected from previous errors
    prompt_style = PromptStyle.from_dict({
        'prompt': 'bold green',
    })

    # 1. check for all AVAILABLE providers
    providers = ["openai", "mistral", "anthropic", "deepseek", "gemini", "ollama"]
    available_providers = []
    
    with Status("[bold green]Loading available providers...", spinner="dots") as status:
        # Create a nice table for providers
        provider_table = Table(show_header=True, header_style="bold green")
        provider_table.add_column("#", style="dim", width=4)
        provider_table.add_column("Provider", style="green")
        provider_table.add_column("Available Models", style="cyan", justify="right")
        
        # First, collect all available providers
        for provider in providers:
            status.update(f"[bold green]Checking provider: [cyan]{provider}[/cyan]...")
            models = retrieve_models(provider)
            if models != []:
                available_providers.append((provider, len(models)))
        
        # Then add them to the table with sequential numbering
        for idx, (provider, model_count) in enumerate(available_providers, start=1):
            provider_table.add_row(
                str(idx), 
                provider, 
                f"{model_count} models"
            )
    
    console.print("")
    console.print(provider_table)
    console.print("")
    
    # If no providers are available, show an error and exit
    if not available_providers:
        console.print(Panel(
            "[bold red]No available providers found.[/bold red]\n"
            "[yellow]Please check your API keys or network connection.[/yellow]",
            title="Error",
            border_style="red",
            expand=False
        ))
        return 1
    
    # Now available_providers is a list of tuples (provider_name, model_count)
    # We need to extract just the provider names for later use
    provider_names = [provider for provider, _ in available_providers]
    
    # Create completers for the providers
    # We'll create completers for both provider names and numeric indices
    provider_name_completer = WordCompleter(provider_names)
    provider_idx_completer = WordCompleter([str(i) for i in range(1, len(provider_names) + 1)])
    
    # Combine both completers by creating a session with both options
    provider_session = PromptSession(
        history=FileHistory(history_file),
        auto_suggest=AutoSuggestFromHistory(),
        completer=provider_idx_completer,  # Primary completer is numeric selection
        enable_history_search=True,
        complete_in_thread=True,
        complete_while_typing=True
    )
    
    # Function to handle error display and table redisplay
    def display_provider_error(error_message):
        # First display the table
        display_provider_table()
        # Then display the error below it
        console.print(Panel(
            error_message,
            title="Error",
            border_style="red",
            expand=False
        ))
        console.print("")
    
    # Function to recreate the provider table for redisplay
    def display_provider_table():
        # Create a new table
        table = Table(show_header=True, header_style="bold green")
        table.add_column("#", style="dim", width=4)
        table.add_column("Provider", style="green")
        table.add_column("Available Models", style="cyan", justify="right")
        
        # Add rows
        for idx, (provider, model_count) in enumerate(available_providers, start=1):
            table.add_row(
                str(idx), 
                provider, 
                f"{model_count} models"
            )
        
        console.print("")
        console.print(table)

    while True:
        try:
            # Use prompt_toolkit for provider selection
            console.print("[bold green]Select a provider[/bold green]")
            prompt_result = provider_session.prompt(
                ">>> ", 
                style=prompt_style,
            )
            
            if prompt_result.strip() == "":
                prompt_result = "1"
                
            # Check if the input is a provider name directly
            if prompt_result in provider_names:
                provider = prompt_result
                provider_idx = provider_names.index(provider)
                console.print(f"[bold green]Selected provider:[/bold green] [bold cyan]{provider}[/bold cyan]")
                break
                
            try:
                provider_idx = int(prompt_result) - 1
                if 0 <= provider_idx < len(provider_names):
                    provider = provider_names[provider_idx]
                    console.print(f"[bold green]Selected provider:[/bold green] [bold cyan]{provider}[/bold cyan]")
                    break
                else:
                    # Display the table first, then the error
                    display_provider_error(f"Please enter a number between 1 and {len(provider_names)}")
            except ValueError:
                # Display the table first, then the error
                display_provider_error("Please enter a valid number or provider name")
        except KeyboardInterrupt:
            console.print("\n", Panel("Interrupted. Please select a provider to continue.", border_style="yellow", expand=False))
        except EOFError:
            console.print("\n[bold red]Exiting...[/bold red]")
            return 1

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
    
    # Create completers for models too
    model_idx_completer = WordCompleter([str(i) for i in range(1, len(models) + 1)])
    model_name_completer = WordCompleter(models)
    
    # Create a session with model options
    model_session = PromptSession(
        history=FileHistory(history_file),
        auto_suggest=AutoSuggestFromHistory(),
        completer=model_idx_completer,  # Primary completer is numeric selection
        enable_history_search=True,
        complete_in_thread=True,
        complete_while_typing=True
    )
    
    # Function to handle error display and table redisplay for models
    def display_model_error(error_message):
        # First display the table
        display_model_table()
        # Then display the error below it
        console.print(Panel(
            error_message,
            title="Error",
            border_style="red",
            expand=False
        ))
        console.print("")
    
    # Function to recreate the model table for redisplay
    def display_model_table():
        # Create a new table
        table = Table(show_header=True, header_style="bold green")
        table.add_column("#", style="dim", width=4)
        table.add_column("Model", style="green")
        
        # Add rows
        for i, model_name in enumerate(models, start=1):
            table.add_row(str(i), model_name)
        
        console.print("")
        console.print(table)

    while True:
        try:
            # Use prompt_toolkit for model selection
            console.print("[bold green]Select a model[/bold green]")
            prompt_result = model_session.prompt(
                ">>> ", 
                style=prompt_style,
            )
            
            if prompt_result.strip() == "":
                prompt_result = "1"
                
            # Check if the input is a model name directly
            if prompt_result in models:
                model = prompt_result
                model_idx = models.index(model)
                console.print(f"[bold green]Selected model:[/bold green] [bold cyan]{model}[/bold cyan]")
                break
                
            try:
                model_idx = int(prompt_result) - 1
                if 0 <= model_idx < len(models):
                    model = models[model_idx]
                    console.print(f"[bold green]Selected model:[/bold green] [bold cyan]{model}[/bold cyan]")
                    break
                else:
                    # Display the table first, then the error
                    display_model_error(f"Please enter a number between 1 and {len(models)}")
            except ValueError:
                # Display the table first, then the error
                display_model_error("Please enter a valid number or model name")
        except KeyboardInterrupt:
            console.print("\n", Panel("Interrupted. Please select a model to continue.", border_style="yellow", expand=False))
        except EOFError:
            console.print("\n[bold red]Exiting...[/bold red]")
            return 1

    # Show startup message
    console.print("")
    console.print(Panel(
        f"[bold]Starting chat with [green]{provider}[/green]/[cyan]{model}[/cyan][/bold]",
        border_style="green",
        expand=False
    ))
    
    # 3. launch the chat in a loop (handle signals EOF, SIGINT, SIGTERM)
    chat(provider, model)
    return 0

def run_with_model(arg):
    console = Console()

    # 1. parse the argument to get the provider and model

    # 2. check if the provider and model are available

    # 3. launch the chat in a loop (handle signals EOF, SIGINT, SIGTERM)


def run_with_model_and_prompt(arg1, arg2):
    console = Console()

    # 1. parse the argument to get the provider and model
    # Parse the provider and model from arg1 (format: provider/modelname)
    parts = arg1.split('/', 1)
    if len(parts) != 2:
        console.print(Panel(
            f"[bold red]Invalid format: {arg1}[/bold red]\nExpected format: provider/modelname",
            title="Error",
            border_style="red",
            expand=False
        ))
        return 1
    
    provider, model = parts
    
    # Check if the provider is available
    with Status(f"[bold green]Checking if provider [cyan]{provider}[/cyan] is available...", spinner="dots") as status:
        available_providers = get_available_providers()
        
        if provider not in available_providers:
            console.print(Panel(
                f"[bold red]Provider '{provider}' not found![/bold red]\nAvailable providers: {', '.join(available_providers)}",
                title="Error",
                border_style="red",
                expand=False
            ))
            return 1
        
        # Check if the model is available for this provider
        models = retrieve_models(provider)
        if model not in models:
            # Stop the status spinner before showing the error message
            status.stop()
            console.print(Panel(
                f"[bold red]Model '{model}' not found for provider '{provider}'![/bold red]\nAvailable models: {', '.join(models[:10])}{'...' if len(models) > 10 else ''}",
                title="Error",
                border_style="red",
                expand=False
            ))
            return 1


    # Get the prompt from arg2
    prompt = arg2
    
    console.print(Panel(
        f"[bold]Using [green]{provider}[/green]/[cyan]{model}[/cyan] to answer:[/bold]\n{prompt}",
        border_style="blue",
        expand=False
    ))

    # 3. Send a single request to the model
    result = single_completion(provider, model, prompt)
    
    # If there's no output (which is the case with ollama since it streams directly)
    # we should at least provide some feedback that we're done
    if result is None or result == "":
        console.print("\n\n[bold green]Completion finished.[/bold green]")
    
    return 0
