import anthropic
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
from io import StringIO

def get_anthropic_models(api_key):
    """Get all models from the Anthropic API"""
    try:
        client = anthropic.Anthropic(api_key=api_key)
        models = client.models.list()
        res = [model.id for model in models]
        return res
    except Exception as e:
        return []


def anthropic_single_completion(model, prompt, api_key):
    console = Console()
    
    try:
        # Use StringIO to collect the full response
        full_response = StringIO()
        output_produced = False
        
        # Print a panel header to indicate streaming is starting
        console.print(Panel(
            "[italic]Generating response...[/italic]",
            title=f"[bold blue]{model}[/bold blue] response",
            border_style="cyan",
            padding=(0, 1),
            expand=False
        ))
        
        # Start on a new line for streaming output
        console.print("", end="")
        
        client = anthropic.Anthropic(api_key=api_key)
        stream = client.messages.create(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=model,
            stream=True,
        )
        
        for event in stream:
            # Specifically check for content block deltas which contain text
            if hasattr(event, 'type') and event.type == 'content_block_delta' and hasattr(event, 'delta'):
                if hasattr(event.delta, 'text') and event.delta.text:
                    content = event.delta.text
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
        return str(e)


def anthropic_chat_completion(model, prompt, messages, api_key):
    """Send a chat request to the model"""
    console = Console()
    console.print(f"[bold blue]{model}[/bold blue] response")
    return ""