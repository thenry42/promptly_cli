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


def gemini_chat_completion(model, prompt, messages, api_key):
    """Send a chat request to the model"""
    console = Console()
    
    try:
        client = genai.Client(api_key=api_key)
        
        # Prepare the content for Gemini
        # For Gemini, we need to convert the message history into a structured content format
        gemini_content = []
        
        if messages:
            # Convert the message history into a text representation that Gemini can understand
            conversation_text = ""
            for msg in messages:
                role = msg["role"]
                content = msg["content"]
                
                # Format each message with a clear role indicator
                if role == "user":
                    conversation_text += f"User: {content}\n\n"
                elif role == "assistant":
                    conversation_text += f"Assistant: {content}\n\n"
            
            # Add the conversation history to the content
            gemini_content.append(conversation_text)
        
        # Add the current prompt if provided
        if prompt:
            if gemini_content:
                gemini_content.append(f"User: {prompt}")
            else:
                gemini_content.append(prompt)
        
        # Join the content parts together
        final_content = "\n".join(gemini_content) if gemini_content else ""
        
        # If no content, return early
        if not final_content:
            console.print("[bold yellow]Warning: No content to send to the model[/bold yellow]")
            return ""
        
        # Use StringIO objects to collect the response text
        full_response = StringIO()
        
        # Track if we've printed anything
        output_produced = False
        
        # Display a fancy animated loading indicator
        with console.status(f"[bold blue]{model}[/bold blue] is thinking...", spinner="dots12") as status:
            # Create the streaming request using the API method we know works
            response = client.models.generate_content_stream(
                model=model,
                contents=final_content,
            )
            
            # Process the streaming chunks
            for chunk in response:
                if hasattr(chunk, 'text') and chunk.text:
                    content = chunk.text
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