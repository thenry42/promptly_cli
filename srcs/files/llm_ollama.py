import ollama
from .config import get_ollama_addr
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
from io import StringIO


def get_ollama_models(addr):
    """Get all models from the Ollama server"""
    try:
        client = ollama.Client(host=addr)
        models = client.list()
        res = [model["model"] for model in models["models"]]
        return res
    except Exception as e:
        return []


def ollama_single_completion(model, prompt):
    """Send a single request to the model"""
    console = Console()
    
    try:
        client = ollama.Client(host=get_ollama_addr())
        response = client.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )
        
        # Use StringIO objects to collect the response text
        full_response = StringIO()
        
        # Track if we've printed anything
        output_produced = False
        
        # Print a panel header first to indicate streaming is starting
        console.print(Panel(
            "[italic]Generating response...[/italic]",
            title=f"[bold blue]{model}[/bold blue] response",
            border_style="cyan",
            padding=(0, 1),
            expand=False
        ))
        
        # For streaming display, we'll print plain text as it comes in
        console.print("", end="")  # Start on a new line
        for chunk in response:
            content = ""
            if "message" in chunk and "content" in chunk["message"]:
                content = chunk["message"]["content"]
            elif "response" in chunk:
                content = chunk["response"]
                
            if content:
                console.print(content, end="")
                full_response.write(content)
                output_produced = True
        
        # Print a newline for proper spacing
        console.print("\n")
        
        # If we got a response, render it as markdown inside a panel
        if output_produced:
            # Get the complete text
            text_response = full_response.getvalue()
            
            # 1. Display plaintext response in a panel
            plaintext_panel = Panel(
                Text(text_response),
                title=f"[bold blue]{model}[/bold blue] response",
                subtitle="Plaintext output",
                border_style="cyan",
                padding=(1, 2),
                expand=False
            )
            console.print(plaintext_panel)
            
            # Add a small separator
            console.print("")
            
            # 2. Display markdown response in a panel
            md = Markdown(text_response)
            markdown_panel = Panel(
                md,
                title=f"[bold blue]{model}[/bold blue] response",
                subtitle="Rendered as Markdown",
                border_style="green",
                padding=(1, 2),
                expand=False
            )
            console.print(markdown_panel)
            console.print()
            
            return "Output displayed in both formats"
        else:
            return ""
            
    except Exception as e:
        console.print(f"\n[bold red]Error: {str(e)}[/bold red]")
        return ""


def ollama_chat_completion(model, prompt, messages):
    """Send a chat request to the model"""
    console = Console()
    
    try:
        client = ollama.Client(host=get_ollama_addr())
        
        # Prepare messages format - append the new prompt
        chat_messages = messages.copy() if messages else []
        if prompt:
            chat_messages.append({"role": "user", "content": prompt})
        
        # If no messages, return early
        if not chat_messages:
            console.print("[bold yellow]Warning: No messages to send to the model[/bold yellow]")
            return ""
        
        response = client.chat(
            model=model,
            messages=chat_messages,
            stream=True
        )
        
        # Use StringIO objects to collect the response text
        full_response = StringIO()
        
        # Track if we've printed anything
        output_produced = False
        
        # Display a fancy animated loading indicator
        with console.status(f"[bold blue]{model}[/bold blue] is thinking...", spinner="dots12") as status:
            # For streaming display, we'll accumulate the response first
            for chunk in response:
                content = ""
                if "message" in chunk and "content" in chunk["message"]:
                    content = chunk["message"]["content"]
                elif "response" in chunk:
                    content = chunk["response"]
                    
                if content:
                    # Just accumulate the response without printing incrementally
                    full_response.write(content)
                    output_produced = True
        
        # If we got a response, render it as markdown inside a panel
        if output_produced:
            # Get the complete text
            text_response = full_response.getvalue()
            
            # Add a newline before displaying the response
            console.print("")
            
            # Display only the markdown response in a panel (no plaintext panel)
            md = Markdown(text_response)
            markdown_panel = Panel(
                md,
                title=f"[bold blue]{model}[/bold blue] response",
                border_style="green",
                padding=(1, 2),
                expand=False
            )
            console.print(markdown_panel)
            console.print()
            
            # Return the generated text response
            return text_response
        else:
            return ""
            
    except Exception as e:
        console.print(f"\n[bold red]Error: {str(e)}[/bold red]")
        return ""
    
