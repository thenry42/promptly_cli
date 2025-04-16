from files.config import get_available_providers, get_ollama_addr
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.box import ROUNDED
from rich.progress import Progress, SpinnerColumn, TextColumn
from .llm_global import retrieve_models

def list_models():
    console = Console()
    providers = ["openai", "mistral", "anthropic", "deepseek", "gemini", "ollama"]
    
    # 1. Get all providers with API keys
    keys = get_available_providers()
    if "ollama" in keys:
        keys.remove("ollama")
        #console.print(f"[green]Ollama address: {get_ollama_addr()}[/green]")
    #console.print(f"[green]Providers with API keys: {keys}[/green]")

    # 2. Get all models for each provider with a spinner
    keys.append("ollama")
    all_models = {}
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]Fetching models..."),
        console=console
    ) as progress:
        progress.add_task("Fetching", total=None)
        for provider in keys:
            models = retrieve_models(provider)
            # Include empty model lists to track providers that returned no models
            all_models[provider] = models if models else []

    # 3. Print all models in gorgeous tables
    if all(len(models) == 0 for models in all_models.values()):
        console.print(Panel.fit(
            "[yellow]No models found for any provider.[/yellow]\n"
            "[yellow]Please check your API keys and connections.[/yellow]",
            title="[bold red]No Models Available",
            border_style="red"
        ))
        return
        
    console.print()
    console.print(Text("🤖 Available Language Models", style="bold cyan underline", justify="center"))
    console.print()
    
    # Track providers with issues to list them at the end
    error_providers = []
    
    # Create tables for each provider with models
    for provider, models in all_models.items():
        # Create provider header with appropriate color
        provider_colors = {
            "openai": "green",
            "mistral": "blue",
            "anthropic": "magenta",
            "deepseek": "yellow",
            "gemini": "cyan",
            "ollama": "red"
        }
        color = provider_colors.get(provider, "white")
        
        # Check if provider has models
        if not models:
            error_providers.append((provider, color))
            continue
        
        # Create a table for this provider - removed show_header
        table = Table(
            show_header=False,  # Removed table header
            box=ROUNDED,
            title=f"{provider.upper()} Models",
            title_style=f"bold {color}",
            expand=True
        )
        
        # Check the format of the models
        if provider == "ollama" and models and isinstance(models[0], dict):
            # Add columns but they won't be displayed as headers
            table.add_column(style=color)  # Model name column
            table.add_column(style="dim")  # Size column
            table.add_column(style="italic")  # Family column
            
            # Sort models alphabetically
            sorted_models = sorted(models, key=lambda x: x.get('name', '').lower())
            
            # Add rows
            for model in sorted_models:
                name = model.get('name', 'Unknown')
                size = model.get('size', 'Unknown')
                family = model.get('family', 'Unknown')
                
                # Format size in GB if available
                if isinstance(size, int) and size > 0:
                    size = f"{size / 1_000_000_000:.2f} GB"
                
                table.add_row(name, size, family)
        else:
            # For other providers or string-based models
            table.add_column(style=color)  # Single column with no header
            
            # Sort models alphabetically 
            if isinstance(models, list):
                # Handle different model formats - could be strings, dicts, or other objects
                sorted_models = []
                for model in models:
                    if isinstance(model, dict) and 'name' in model:
                        sorted_models.append(model['name'])
                    elif isinstance(model, str):
                        sorted_models.append(model)
                    else:
                        # Try to convert the model to a string
                        sorted_models.append(str(model))
                
                # Sort the model names
                sorted_models.sort(key=str.lower)
                
                # Add rows
                for model_name in sorted_models:
                    table.add_row(model_name)
        
        # Display the table in a panel
        console.print(Panel(
            table,
            border_style=color,
            padding=(1, 2)
        ))
        console.print()  # Add some space between providers
    
    # Show providers with zero models
    if error_providers:
        issue_table = Table(
            show_header=False,
            box=ROUNDED,
            title="Providers With Issues",
            title_style="bold red",
            expand=True
        )
        
        issue_table.add_column(style="red")
        issue_table.add_column(style="yellow", ratio=3)
        
        for provider, color in error_providers:
            issue_table.add_row(
                f"[bold {color}]{provider.upper()}[/bold {color}]",
                "[yellow]No models found. Possible API key or connection issue.[/yellow]"
            )
        
        console.print(Panel(
            issue_table,
            border_style="red",
            padding=(1, 2)
        ))
        
        # Add troubleshooting tips
        console.print(Panel(
            "[bold white]Troubleshooting Tips:[/bold white]\n"
            "• Check that your API keys are valid and not expired\n"
            "• Verify your internet connection\n"
            "• For Ollama, ensure the server is running locally (usually http://localhost:11434)",
            title="[bold red]How to Fix",
            border_style="yellow"
        ))
    