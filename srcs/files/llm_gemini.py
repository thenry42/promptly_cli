from google import genai
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
from io import StringIO


def get_gemini_models(api_key):
    """Get all models from the Gemini API"""
    try:
        client = genai.Client(api_key=api_key)
        models = client.models.list()
        res = [model.name for model in models]
        return res
    except Exception as e:
        return []


def gemini_single_completion(model, prompt, api_key):
    console = Console()
    try:
        full_response = StringIO()
        output_produced = False

        console.print(Panel(
            "[italic]Generating response...[/italic]",
            title=f"[bold blue]{model}[/bold blue] response",
            border_style="cyan",
            padding=(0, 1),
            expand=False
        ))

        console.print("", end="")

        client = genai.Client(api_key=api_key)
        response = client.models.generate_content_stream(
            model=model,
            contents=prompt,
        )
        
        for chunk in response:
            if hasattr(chunk, 'text') and chunk.text:
                content = chunk.text
                console.print(content, end="")
                full_response.write(content)
                output_produced = True
        
        # Print a newline for proper spacing
        console.print("\n")

        if output_produced:
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
