from files.style import CSS
from textual.app import App, ComposeResult
from textual.widgets import Header, Input, Static, OptionList
from textual.containers import VerticalScroll, Horizontal
from files.bindings import BINDINGS
from textual import events
from files.actions import Actions
from files.options_list import OptionsList


class ShellApp(App):
    """A terminal application for running LLMs in a text-based interface."""

    CSS = CSS
    BINDINGS = BINDINGS
    ENABLE_COMMAND_PALETTE = False
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.command_history = []
        self.history_index = 0
        self.theme = "nord"
        self.actions = Actions(self)
        self.options = OptionsList(self)
        self.prompt = "$> "
    
    def on_mount(self) -> None:
        """Initialize the UI when the app is mounted."""
        self.query_one("#option-list").display = False
        
        output = self.query_one("#terminal-output", VerticalScroll)
        output.mount(Static("Welcome to SheLLM!", classes="output-line"))
        output.mount(Static("Type commands below:", classes="output-line"))
        output.mount(Static("Try typing 'new' to see available options", classes="output-line"))
        
        # Create the initial prompt with input field
        self.create_new_prompt()
        
        # Ensure input is focused
        self.set_timer(0.1, self.focus_input)
    
    def on_screen_resume(self) -> None:
        """Ensure input is focused when screen resumes."""
        self.set_timer(0.1, self.focus_input)
    
    def create_new_prompt(self) -> None:
        """Creates a new prompt line with input field."""
        terminal = self.query_one("#terminal-output")
        
        # First, create a container for the prompt and input
        prompt_container = Horizontal(classes="prompt-container")
        terminal.mount(prompt_container)
        
        # Now that the container is mounted, add the prompt text
        prompt_container.mount(Static(self.prompt, classes="prompt"))
        
        # Create and add the input field
        input_field = Input(id="command-input")
        prompt_container.mount(input_field)
        
        # Focus the input
        input_field.focus()
        
        # Scroll to make the prompt visible
        terminal.scroll_end(animate=False)
        
        # Ensure focus with a slight delay
        self.set_timer(0.1, self.focus_input)
    
    def compose(self) -> ComposeResult:
        """Compose the UI elements."""
        yield Header(show_clock=True, time_format="%H:%M:%S")
        
        with VerticalScroll(id="terminal-output"):
            pass
        
        yield OptionList(
            "Create a new chat",
            "New terminal session",
            "Cancel",
            id="option-list"
        )
    
    def on_input_submitted(self, event) -> None:
        """Process command input when submitted."""
        if event.input.id != "command-input":
            return
            
        command = event.value.strip()
        
        # Remove the current prompt container
        prompt_container = event.input.parent
        prompt_container.remove()
        
        if not command:
            self.create_new_prompt()
            return
            
        # Add command to history before processing
        self.command_history.append(command)
        self.history_index = len(self.command_history)
        
        output = self.query_one("#terminal-output")
        
        # Process the command
        if command == "hello":
            self.actions.action_say_hello()
            output.mount(Static("Hello, world!", classes="output-line"))
        elif command == "theme":
            self.actions.action_toggle_theme()
            output.mount(Static(f"Theme switched to {self.theme}", classes="output-line"))
        elif command == "help":
            self.action_help()
        elif command == "exit":
            self.exit()
        elif command == "clear":
            # Clear terminal output but keep a clean state
            output.remove_children()
            output.mount(Static("Terminal cleared", classes="output-line"))
        elif command == "new":
            self.options.show_option_list()
            output.mount(Static("Select an option to create:", classes="output-line"))
        else:
            output.mount(Static(f"Unknown command: {command}", classes="output-line error"))
        
        # Create a new prompt immediately after the response
        self.create_new_prompt()
    
    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        """Handle option list selection."""
        self.options.on_option_list_option_selected(event)
    
    def on_key(self, event) -> None:
        """Handle key events for command history navigation."""
        try:
            # Check for an active input field
            input_widget = self.query_one("#command-input", Input)
            
            # Only handle arrow keys when input has focus and we have command history
            if not input_widget.has_focus or not self.command_history:
                return
                
            if event.key == "up":
                # Navigate to previous command in history
                if self.history_index > 0:
                    self.history_index -= 1
                    input_widget.value = self.command_history[self.history_index]
                    input_widget.cursor_position = len(input_widget.value)
                    event.prevent_default()
            
            elif event.key == "down":
                # Navigate to next command in history or clear if at the end
                if self.history_index < len(self.command_history) - 1:
                    self.history_index += 1
                    input_widget.value = self.command_history[self.history_index]
                    input_widget.cursor_position = len(input_widget.value)
                elif self.history_index == len(self.command_history) - 1:
                    # At the end of history, clear the input
                    self.history_index = len(self.command_history)
                    input_widget.value = ""
                event.prevent_default()
                
        except Exception as e:
            # If there's an error (like no input field found), just continue
            pass
    
    def on_blur(self, event: events.Blur) -> None:
        """Redirect focus to input when other elements lose focus."""
        option_list = self.query_one("#option-list")
        
        # Don't redirect focus if we're closing the app
        if self.is_closing:
            return
            
        # Don't redirect if we just lost focus from the input itself
        if event.target.id == "command-input":
            return
            
        # Don't redirect if the option list is visible and has focus
        if option_list.display and option_list.has_focus:
            return
            
        # In all other cases, refocus the input field
        self.set_timer(0.05, self.focus_input)
    
    def focus_input(self) -> None:
        """Focus the input field."""
        try:
            # Check if the option list is visible
            option_list = self.query_one("#option-list")
            if option_list.display:
                # Don't focus input if option list is visible
                return
                
            # Find and focus the input field
            input_field = self.query_one("#command-input")
            if not input_field.has_focus:
                input_field.focus()
        except Exception:
            # Input might not exist yet
            pass
            
    def on_click(self, event: events.Click) -> None:
        """Ensure input focus is maintained on click events."""
        # Don't redirect if we're clicking on the option list
        option_list = self.query_one("#option-list")
        if option_list.display:
            return
            
        # Focus the input on any click in the app (after a short delay)
        self.set_timer(0.05, self.focus_input)
    
    def action_toggle_theme(self) -> None:
        """Toggle between themes."""
        self.actions.action_toggle_theme()

    def action_say_hello(self) -> None:
        """Display a hello message."""
        self.actions.action_say_hello()

    def action_exit(self) -> None:
        """Exit the application."""
        self.exit()
    
    def action_help(self) -> None:
        """Show help information in the terminal."""
        self.actions.action_help()
    
