from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, Input, Static
from prompt_toolkit.history import InMemoryHistory
from files.commands import *

class CommandOutput(Static):
    """Widget to display command output."""
    pass

class CommandApp(App):
    """Terminal application with a border."""
    
    CSS = """
    Screen {
        layout: grid;
        grid-size: 1;
        grid-gutter: 0;
        padding: 1;
    }
    
    #command-container {
        width: 100%;
        height: 100%;
        border: solid $accent;
        padding: 1;
    }
    
    #output {
        height: 1fr;
        overflow-y: auto;
    }
    
    #command-input {
        margin-top: 1;
    }
    """
    
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        
        with Container(id="command-container"):
            yield CommandOutput("Welcome to the Command Application\n", id="output")
            yield Input(placeholder="Enter command...", id="command-input")
        
        yield Footer()
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Process commands when Enter is pressed."""
        command = event.value
        
        # Add command to output
        output = self.query_one("#output")
        output.update(output.render().plain + f"> {command}\n")
        
        # Process command
        if command.lower() in ("exit", "quit"):
            output.update(output.render().plain + "See you next time!\n")
            self.exit()
        else:
            # Here you'd integrate with handle_command
            output.update(output.render().plain + f"Processing: {command}\n")
        
        # Clear input
        event.input.value = ""


if __name__ == "__main__":
    app = CommandApp()
    app.run()