from textual.widgets import Static


class Actions:
    """Handles application actions and commands."""
    
    def __init__(self, app):
        self.app = app

    def action_toggle_theme(self) -> None:
        """Toggle between available themes."""
        self.app.theme = "nord" if self.app.theme == "gruvbox" else "gruvbox"
        self.app.focus_input()

    def action_say_hello(self) -> None:
        """Display a greeting notification."""
        self.app.notify("Hello, world!", title="Greeting")
        self.app.focus_input()

    def action_exit(self) -> None:
        """Exit the application."""
        self.app.exit()

    def action_help(self) -> None:
        """Show help information in the terminal."""
        output = self.app.query_one("#terminal-output")
        output.mount(Static("Available commands:", classes="output-line"))
        output.mount(Static("  hello - Display a greeting", classes="output-line"))
        output.mount(Static("  theme - Toggle between themes", classes="output-line"))
        output.mount(Static("  clear - Clear the terminal", classes="output-line"))
        output.mount(Static("  new   - Create a new chat or session", classes="output-line"))
        output.mount(Static("  exit  - Exit the application", classes="output-line"))
        output.mount(Static("Keyboard shortcuts:", classes="output-line"))
        output.mount(Static("  Ctrl+T - Toggle theme", classes="output-line"))
        output.mount(Static("  Ctrl+H - Show help", classes="output-line"))
        output.mount(Static("  Ctrl+L - Clear terminal", classes="output-line"))
        output.mount(Static("  Ctrl+N - Create new", classes="output-line"))
        output.mount(Static("  Ctrl+Q/Ctrl+D - Exit", classes="output-line"))
    
    def action_new(self) -> None:
        """Show options for creating new items."""
        self.app.options.show_option_list()
        