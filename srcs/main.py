from rich.console import Console
from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from time import sleep


def main():
    console = Console()
    history = InMemoryHistory()

    while True:
        try:
            user_input = prompt("> ", history=history)
            if user_input in ("exit", "quit"):
                console.print("[bold red]See you next time![/bold red]")
                sleep(0.5)
                break
            console.print(f"[bold cyan]You typed:[/bold cyan] {user_input}")
        except (KeyboardInterrupt, EOFError):
            console.print("[bold red]See you next time![/bold red]")
            sleep(0.5)
            break


if __name__ == "__main__":
    main()