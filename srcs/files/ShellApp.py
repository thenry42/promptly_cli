from files.style import CSS
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input
from files.bindings import BINDINGS
from textual import events
from files.palette_commands import PaletteCommands


class ShellApp(App):
    """
    A terminal application that allows you to run LLMs and much more.
    Textual & rich are used to create a good looking terminal.
    """

    CSS = CSS
    BINDINGS = BINDINGS
    COMMANDS = {PaletteCommands}


    
    def on_mount(self) -> None:
        """
        On mount, set the history and theme.
        Init function pretty much.
        """
        self.theme = "nord"

    
    def compose(self) -> ComposeResult:
        """Compose the UI"""
        yield Header()
        yield Footer()


    def action_toggle_theme(self) -> None:
        """Toggle theme."""
        self.theme = (
            "nord" if self.theme == "gruvbox" else "gruvbox"
        )


    def action_say_hello(self) -> None:
        """Say hello to the user."""
        self.notify("Hello, World!", title="Greeting")


    def action_exit(self) -> None:
        """Exit the application."""
        self.exit()
