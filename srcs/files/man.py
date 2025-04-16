from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.markdown import Markdown
from .list import list_models, list_models_with_provider
from .run import run_no_args, run_with_model, run_with_model_and_prompt


def Usage():
    console = Console()
    
    # Create a stylish header
    header = Text("Promptly CLI", style="bold cyan")
    subheader = Text("A command-line interface for language models", style="italic")
    
    # Create a command table with explicit width settings
    table = Table(show_header=True, header_style="bold magenta", expand=True)
    table.add_column("Command", style="green", no_wrap=False)
    table.add_column("Description", style="yellow", ratio=3)
    
    # Add commands to the table
    table.add_row("llm list", "Show available models")
    table.add_row("llm list \\[provider]", "Show available models for a specific provider")
    table.add_row("llm run \\[model]", "Run a model in interactive mode")
    table.add_row("llm run \\[model] \\[prompt]", "Run a model with a single request")
    table.add_row("llm help", "Help about any command")
    
    # Display everything in panels that adapt to console width
    console.print()
    console.print(Panel(
        f"{header}\n{subheader}",
        title="[bold white]About",
        border_style="blue"
    ))
    console.print()
    console.print(Panel(
        table,
        title="[bold white]Available Commands",
        border_style="green"
    ))
    console.print()


def list(args):
    console = Console()
    if len(args) == 1: # llm list = 1 arg
        list_models()
    elif len(args) == 2: # llm list [provider] = 2 args
        list_models_with_provider(args[1])
    else:
        console.print("Error: Invalid number of arguments. Expected 1 or 2 arguments, got", len(args))


def run(args):
    console = Console()
    if len(args) == 1: # llm run = 1 arg
        run_no_args()
    elif len(args) == 2: # llm run [model] = 2 args
        run_with_model(args[1])
    elif len(args) == 3: # llm run [model] [prompt] = 3 args
        run_with_model_and_prompt(args[1], args[2])
    else:
        console.print("Error: Invalid number of arguments. Expected 2 or 3 arguments, got", len(args))


def help():
    console = Console()
    # Create a command table with explicit width settings
    table = Table(show_header=True, header_style="bold magenta", expand=True)
    table.add_column("Command", style="green", no_wrap=False)
    table.add_column("Description", style="yellow", ratio=3)
    
    # Add commands to the table
    table.add_row("llm list", "Show available models")
    table.add_row("llm list \\[provider]", "Show available models for a specific provider")
    table.add_row("llm run", "Launch a chat with a model in interactive mode.")
    table.add_row("llm run \\[provider]/\\[model]", "Run a specific model in interactive mode")
    table.add_row("llm run \\[provider]/\\[model] \\[prompt]", "Run a specific model with a single request")
    table.add_row("llm help", "Help about any command")
    
    console.print()
    console.print(Panel(
        table,
        title="[bold white]Available Commands",
        border_style="green"
    ))
    console.print()