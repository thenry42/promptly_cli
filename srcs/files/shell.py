from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text
from rich.theme import Theme
import os
import sys
from .providers import get_providers

# Custom theme
custom_theme = Theme({
    "prompt": "green bold",
    "command": "green",
    "error": "red",
    "info": "cyan",
    "header": "magenta bold"
})

console = Console(theme=custom_theme)

class Shell:
    def __init__(self):
        self.command_history = []
        self.history_index = 0
        self.running = True
        self.prompt = "> "
        self.theme = "default"
    
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
        
        # Add to history
        self.command_history.append(command)
        self.history_index = len(self.command_history)
        
        # Process commands
        if command == "hello":
            console.print("Hello, world!", style="info")
        elif command == "theme":
            self.theme = "dark" if self.theme == "default" else "default"
            console.print(f"Theme switched to {self.theme}", style="info")
        elif command == "help":
            self.show_help()
        elif command == "providers":
            self.show_providers()
        elif command == "exit":
            console.print("Exiting...", style="info")
            self.running = False
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
            ("theme", "Toggle between themes"),
            ("clear", "Clear the terminal"),
            ("providers", "Show available AI providers"),
            ("exit", "Exit the application")
        ]
        
        for cmd, desc in commands:
            console.print(f"  {cmd} - {desc}")
        
        console.print()
    
    def show_providers(self):
        """Show available providers."""
        providers = get_providers()
        console.print()
        console.print("Available providers:", style="info")
        for provider in providers:
            console.print(f"- {provider}")
        console.print()
    
    def main_loop(self):
        """Main application loop."""
        self.clear_screen()
        
        while self.running:
            try:
                # Display the styled prompt
                console.print(self.prompt, end="", style="prompt")
                # Get user input without styling
                command = input()
                self.execute_command(command)
            except KeyboardInterrupt:
                console.print("\nUse 'exit' to quit", style="info")
            except Exception as e:
                console.print(f"Error: {e}", style="error")
        
        console.print("Goodbye!", style="info")
