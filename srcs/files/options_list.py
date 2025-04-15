from textual.widgets import OptionList
from textual.widgets import Static


class OptionsList:
    """Manages option list functionality for the application."""
    
    def __init__(self, app):
        self.app = app

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        """Handle option selection from the option list."""
        option = event.option.prompt
        output = self.app.query_one("#terminal-output")
        
        # First hide the option list
        self.app.query_one("#option-list").display = False
         
        try:
            for container in output.query(".prompt-container"):
                container.remove()
        except Exception:
            pass
        
        # Then show the appropriate message
        if option == "Create a new chat":
            output.mount(Static("Creating a new file...", classes="output-line"))
        elif option == "New terminal session":
            output.mount(Static("Starting a new terminal session...", classes="output-line"))
        elif option == "Cancel":
            output.mount(Static("Cancelling...", classes="output-line"))
        
        # After showing the message, create a new prompt
        self.app.create_new_prompt()
        
        # Finally, focus the input field
        self.app.set_timer(0.1, self.app.focus_input)
    
    def show_option_list(self) -> None:
        """Display the option list for creating new items."""
        option_list = self.app.query_one("#option-list")
        option_list.display = True
        self.app.set_timer(0.1, self._focus_option_list)
        
        output = self.app.query_one("#terminal-output")
        output.mount(Static("Use ↑/↓ arrows to navigate, Enter to select, Esc to cancel", 
                          classes="output-line hint"))

    def _focus_option_list(self) -> None:
        """Focus the option list and highlight the first option."""
        option_list = self.app.query_one("#option-list")
        option_list.focus()
        
        if len(option_list.options) > 0:
            option_list.highlighted = 0