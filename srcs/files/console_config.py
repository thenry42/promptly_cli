from rich.console import Console
from rich.theme import Theme

# Custom theme
custom_theme = Theme({
    "prompt": "green bold",
    "command": "green",
    "error": "red",
    "info": "cyan",
    "header": "magenta bold"
})

# Create a shared console instance
console = Console(theme=custom_theme) 