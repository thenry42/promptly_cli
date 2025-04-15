from files.style import CSS
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Static, OptionList
from textual.containers import Container, VerticalScroll
from files.bindings import BINDINGS
from textual import events
from files.palette_commands import PaletteCommands
from rich.text import Text


class ShellApp(App):
    """
    A terminal application that allows you to run LLMs and much more.
    Textual & rich are used to create a good looking terminal.
    """

    CSS = CSS
    BINDINGS = BINDINGS
    COMMANDS = {PaletteCommands}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.command_history = []
        self.history_index = 0
    
    def on_mount(self) -> None:
        """
        On mount, set the history and theme.
        Init function pretty much.
        """
        self.theme = "nord"
        # Hide the help panel initially
        help_panel = self.query_one("#help-panel")
        help_panel.display = False
        
        # Hide the option list initially
        option_list = self.query_one("#option-list")
        option_list.display = False
        
        # Add welcome message
        output = self.query_one("#terminal-output", VerticalScroll)
        output.mount(Static("Welcome to SheLLM!", classes="output-line"))
        output.mount(Static("Type commands below:", classes="output-line"))
        output.mount(Static("Try typing 'new' to see available options", classes="output-line"))
        
        # Auto-focus the input field
        self.query_one("#command-input").focus()
    
    def compose(self) -> ComposeResult:
        """Compose the UI"""
        yield Header()
        
        # Terminal output area
        with VerticalScroll(id="terminal-output"):
            # Output will be added here dynamically
            pass
        
        # Option list (hidden by default)
        option_list = OptionList(
            "Create a new file",
            "Start a new project",
            "Create a new database",
            "New terminal session",
            "New API endpoint",
            id="option-list"
        )
        yield option_list
        
        # Command input with a better placeholder
        yield Input(
            placeholder="Type a command (hello, theme, help, clear, new, exit)...", 
            id="command-input"
        )
        
        # Help panel (hidden by default)
        with Container(id="help-panel"):
            yield Static("## Available Commands", classes="help-title")
            yield Static("- hello: Say Hi to a user", classes="help-command")
            yield Static("- exit: Exit the application", classes="help-command") 
            yield Static("- theme: Switch between themes", classes="help-command")
            yield Static("- help: Toggle this help panel", classes="help-command")
            yield Static("- clear: Clear the terminal", classes="help-command")
            yield Static("- new: Open options for creating new items", classes="help-command")
        
        yield Footer()
    
    def on_input_submitted(self, event: events.Key) -> None:
        """Handle command input submission."""
        # Only process if it's from our command input
        if event.input.id != "command-input":
            return
            
        command = event.value.strip()
        
        # Add command to history
        if command:
            self.command_history.append(command)
            self.history_index = len(self.command_history)
            
            # Get the output area
            output = self.query_one("#terminal-output")
            
            # Display the command
            output.mount(Static(f"$ {command}", classes="command-line"))
            
            # Process the command
            if command == "hello":
                output.mount(Static("Hello, world!", classes="output-line"))
            elif command == "theme":
                self.action_toggle_theme()
                output.mount(Static(f"Theme switched to {self.theme}", classes="output-line"))
            elif command == "help":
                self.action_help()
                output.mount(Static("Help panel toggled", classes="output-line"))
            elif command == "exit":
                self.exit()
            elif command == "clear":
                # Clear terminal output
                output.remove_children()
                output.mount(Static("Terminal cleared", classes="output-line"))
            elif command == "new":
                self.show_option_list()
                output.mount(Static("Select an option to create:", classes="output-line"))
            else:
                output.mount(Static(f"Unknown command: {command}", classes="output-line error"))
            
            # Scroll to the bottom to show latest output
            output.scroll_end(animate=False)
            
            # Clear the input field and re-focus it
            event.input.value = ""
            event.input.focus()
    
    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        """Handle option selection from the option list."""
        option = event.option.prompt
        output = self.query_one("#terminal-output")
        
        # Handle different options
        if option == "Create a new file":
            output.mount(Static("Creating a new file...", classes="output-line"))
            # Implement file creation logic here
        elif option == "Start a new project":
            output.mount(Static("Starting a new project...", classes="output-line"))
            # Implement project creation logic here
        elif option == "Create a new database":
            output.mount(Static("Creating a new database...", classes="output-line"))
            # Implement database creation logic here
        elif option == "New terminal session":
            output.mount(Static("Starting a new terminal session...", classes="output-line"))
            # Implement terminal session logic here
        elif option == "New API endpoint":
            output.mount(Static("Creating a new API endpoint...", classes="output-line"))
            # Implement API endpoint creation logic here
        
        # Hide the option list after selection
        self.query_one("#option-list").display = False
        
        # Scroll to show the latest output
        output.scroll_end(animate=False)
        
        # Re-focus the input
        self.focus_input()
    
    def show_option_list(self) -> None:
        """Show the option list for creating new items."""
        # Get references to the widgets
        option_list = self.query_one("#option-list")
        
        # Make the option list visible first
        option_list.display = True
        
        # Use set_timer to focus the option list after it's been rendered
        # This ensures the focus happens after the display change is processed
        self.set_timer(0.1, self._focus_option_list)
        
        # Add a message to the terminal
        output = self.query_one("#terminal-output")
        output.mount(Static("Use ↑/↓ arrows to navigate, Enter to select, Esc to cancel", 
                          classes="output-line hint"))

    def _focus_option_list(self) -> None:
        """Focus the option list after it's been displayed."""
        option_list = self.query_one("#option-list")
        
        # Focus the option list
        option_list.focus()
        
        # Highlight the first option (if any exist)
        if len(option_list.options) > 0:
            option_list.highlighted = 0
    
    def on_input_key(self, event: events.Key) -> None:
        """Handle key events in the input."""
        # Only process if it's from our command input
        if event.input.id != "command-input":
            return
            
        # History navigation with Up/Down arrow keys
        if event.key == "up" and self.command_history:
            if self.history_index > 0:
                self.history_index -= 1
                event.input.value = self.command_history[self.history_index]
                event.input.cursor_position = len(event.input.value)
                event.prevent_default()
        
        elif event.key == "down" and self.command_history:
            if self.history_index < len(self.command_history) - 1:
                self.history_index += 1
                event.input.value = self.command_history[self.history_index]
                event.input.cursor_position = len(event.input.value)
            elif self.history_index == len(self.command_history) - 1:
                self.history_index = len(self.command_history)
                event.input.value = ""
            event.prevent_default()
        
        # Handle Escape key to close option list if visible
        elif event.key == "escape":
            option_list = self.query_one("#option-list")
            if option_list.display:
                option_list.display = False
                self.focus_input()
                event.prevent_default()
    
    def on_blur(self, event: events.Blur) -> None:
        """When any widget loses focus, redirect focus to the input."""
        # Skip if closing the app or if it's the input field itself losing focus
        # Also skip if the option list is visible and has focus
        option_list = self.query_one("#option-list")
        if (not self.is_closing and 
            event.target.id != "command-input" and 
            not (option_list.display and option_list.has_focus)):
            # Focus the input after a very brief delay to avoid focus loop issues
            self.set_timer(0.05, self.focus_input)
    
    def focus_input(self) -> None:
        """Focus the input field."""
        self.query_one("#command-input").focus()
            
    def action_toggle_theme(self) -> None:
        """Toggle theme."""
        self.theme = (
            "nord" if self.theme == "gruvbox" else "gruvbox"
        )

    def action_say_hello(self) -> None:
        """Say hello to the user."""
        self.notify("Hello, world!", title="Greeting")

    def action_exit(self) -> None:
        """Exit the application."""
        self.exit()
    
    def action_help(self) -> None:
        """Toggle the help panel."""
        help_panel = self.query_one("#help-panel")
        help_panel.display = not help_panel.display
        # Re-focus input after toggling help
        self.focus_input()
    
