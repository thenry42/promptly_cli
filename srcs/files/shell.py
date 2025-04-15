from rich.console import Console
from rich.panel import Panel
from rich.theme import Theme
import os
import sys
import readline  # For history navigation
from .status import get_status
from .console_config import console


class Shell:
    def __init__(self):
        self.command_history = []
        self.history_index = 0
        self.running = True
        self.prompt = "> "
        self.theme = "default"
        
        # Configure readline
        try:
            # Set up history file
            histfile = os.path.join(os.path.expanduser("~"), ".shellm_history")
            try:
                readline.read_history_file(histfile)
                readline.set_history_length(1000)
            except FileNotFoundError:
                pass
                
            # Set the readline prompt directly
            # This is the key fix - readline will now handle the prompt properly
            readline.set_pre_input_hook(lambda: readline.insert_text(''))
            
            # Save history on exit
            import atexit
            atexit.register(readline.write_history_file, histfile)
        except (ImportError, AttributeError):
            pass
    
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
        self.print_header()
    
    def print_header(self):
        """Print the application header."""
        console.print(Panel("SheLLM Terminal", style="header"), justify="center")
        console.print()
    
    def execute_command(self, command):
        """Execute a command and display its output."""
        if command.strip() == "":
            return
        
        # Save command to our history list
        if command not in self.command_history:
            self.command_history.append(command)
        
        # Process commands
        if command == "hello":
            console.print("Hello, world!", style="info")
        elif command == "help":
            self.show_help()
        elif command == "status":
            self.show_status()
        elif command == "exit":
            console.print("Exiting...", style="info")
            self.running = False
            exit()
        elif command == "clear":
            self.clear_screen()
        else:
            console.print(f"Unknown command: {command}. Type 'help' to see available commands.", 
                          style="error")
    
    def show_help(self):
        """Display help information."""
        console.print()
        console.print("Available commands:", style="info")
        commands = [
            ("hello", "Display a greeting"),
            ("clear", "Clear the terminal"),
            ("status", "Show the status of providers"),
            ("exit", "Exit the application")
        ]
        
        for cmd, desc in commands:
            console.print(f"  {cmd} - {desc}")
        
        console.print()
        console.print("Keyboard shortcuts:", style="info")
        console.print("  Up Arrow   - Previous command in history")
        console.print("  Down Arrow - Next command in history")
        console.print("  Ctrl+C     - Interrupt current operation")
        console.print()
    
    def show_status(self):
        """Show available providers."""
        get_status()
        console.print()
    
    def main_loop(self):
        """Main application loop."""
        self.clear_screen()
        
        while self.running:
            try:
                # Use readline's prompt functionality directly
                # This keeps the prompt visible during history navigation
                command = input(console.render_str(f"[prompt]{self.prompt}[/prompt]"))
                self.execute_command(command)
            except KeyboardInterrupt:
                console.print("\nUse 'exit' to quit", style="info")
                continue
            except Exception as e:
                console.print(f"Error: {e}", style="error")
        
        console.print("Goodbye!", style="info")
