from rich.console import Console
from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from time import sleep
from files.commands import *


def main():
    console = Console()
    history = InMemoryHistory()

    while True:
        try:
            user_input = prompt("> ", history=history) # string
            if not handle_command(user_input):
                console.print("[bold red]See you next time![/bold red]")
                sleep(0.5)
                break
        except (KeyboardInterrupt, EOFError):
            console.print("[bold red]See you next time![/bold red]")
            sleep(0.5)
            break


if __name__ == "__main__":
    main()