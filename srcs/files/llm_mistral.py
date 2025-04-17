import mistralai
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
from io import StringIO


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
        
        with mistralai.Mistral(
            api_key=api_key,
        ) as mistral:
            res = mistral.chat.stream(model=model, messages=[
                {
                    "content": prompt,
                    "role": "user",
                },
            ])

            with res as event_stream:
                for event in event_stream:
                    # Only print the content of the delta
                    if event.data.choices[0].delta.content:
                        content = event.data.choices[0].delta.content
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
