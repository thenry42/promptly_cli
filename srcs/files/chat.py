import signal
import readline
from rich.console import Console

def chat(provider, model):
    console = Console()

    def handle_sigint(signum, frame):
        console.print("\n[bold yellow]Prompt interrupted. You can continue typing...[/bold yellow]")
        return 

    console.print("[bold green]Welcome to the AI Chat![/bold green] Type your message and press Enter. Press Ctrl+D to exit.")

    # Initialize readline for input history
    readline.parse_and_bind("tab: complete")
    readline.parse_and_bind("set editing-mode emacs")
    readline.set_completer_delims(' \t\t;')

    while True:
        try:
            signal.signal(signal.SIGINT, handle_sigint)

            # Use input() to leverage readline's history navigation
            user_input = console.input("[bold blue]You: [/bold blue]")
            if user_input.strip() == "":
                continue

            # Add user input to history
            readline.add_history(user_input)

            # Simulate AI response (for now, echoing user input)
            ai_response = user_input  # Replace with actual AI model call
            console.print(f"[bold magenta]AI:[/bold magenta] {ai_response}")

        except EOFError:
            console.print("\n[bold red]Goodbye![/bold red]")
            break
        except KeyboardInterrupt:
            console.print("\n[bold yellow]Starting a new prompt...[/bold yellow]")
            continue

    # Clear the history at the end of the chat
    readline.clear_history()

    return 0