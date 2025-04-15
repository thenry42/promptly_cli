from files.style import CSS
from textual.app import App, ComposeResult
from textual.widgets import Header, Input, Static, OptionList
from textual.containers import VerticalScroll, Horizontal
from textual import events
from files.actions import Actions, BINDINGS


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
        self.prompt = "> "
    
    def on_mount(self) -> None:
        """Initialize the UI when the app is mounted."""
        output = self.query_one("#terminal-output", VerticalScroll)
        
        # Create the initial prompt with input field
        self.create_new_prompt()
        
        # Ensure input is focused
        self.set_timer(0.1, self.focus_input)
    
    def on_screen_resume(self) -> None:
        """Ensure input is focused when screen resumes."""
        self.set_timer(0.1, self.focus_input)
    
    def create_new_prompt(self) -> None:
        """Creates a new prompt line with input field."""
        # Don't create a prompt if the app is closing
        if not self:
            return
            
        try:
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
        except Exception:
            # Handle any errors that might occur during shutdown
            pass
    
    def compose(self) -> ComposeResult:
        """Compose the UI elements."""
        yield Header(show_clock=True, time_format="%H:%M:%S")
        
        with VerticalScroll(id="terminal-output"):
            pass
            
        # Option list is now created dynamically when needed
        # It will be positioned inside the terminal output area
    
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
        
        # Display the command that was entered
        command_text = f"{self.prompt}{command}"
        output.mount(Static(command_text, classes="command-line"))
        
        # Process the command
        if command == "hello":
            self.actions.action_say_hello()
            output.mount(Static("Hello, world!", classes="output-line"))
            self.create_new_prompt()
        elif command == "theme":
            self.actions.action_toggle_theme()
            output.mount(Static(f"Theme switched to {self.theme}", classes="output-line"))
            self.create_new_prompt()
        elif command == "help":
            self.action_help()
            self.create_new_prompt()
        elif command == "exit":
            # Don't create a new prompt when exiting
            output.mount(Static("Exiting...", classes="output-line"))
            self.set_timer(0.5, self.exit)
        elif command == "clear":
            # Clear terminal output
            output.remove_children()
            # After clearing, show a message
            output.mount(Static("Terminal cleared", classes="output-line"))
            self.create_new_prompt()
        else:
            output.mount(Static(f"Unknown command: {command}. Type 'help' to see available commands.", classes="output-line error"))
            self.create_new_prompt()
    
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
        # Don't redirect focus if we're closing the app
        if self.is_closing:
            return
            
        # Don't redirect if we just lost focus from the input itself
        if event.target.id == "command-input":
            return
            
        # In all other cases, refocus the input field
        self.set_timer(0.05, self.focus_input)
    
    def focus_input(self) -> None:
        """Focus the input field."""
        try:
            # Find and focus the input field
            input_field = self.query_one("#command-input")
            if not input_field.has_focus:
                input_field.focus()
        except Exception:
            # Input might not exist yet
            pass
            
    def on_click(self, event: events.Click) -> None:
        """Ensure input focus is maintained on click events."""
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
    
