import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv, set_key
from rich.console import Console

console = Console()

# Get the project root directory (where .env should be located)
PROJECT_ROOT = Path(__file__).parent.parent.parent.absolute()

# Define locations to look for .env files in order of preference
def get_env_file_paths():
    """Get potential .env file paths in order of preference"""
    paths = [
        # 1. Check in the installation directory
        os.path.join(PROJECT_ROOT, '.env'),
        
        # 2. Check in config directory
        os.path.join(os.path.expanduser('~'), '.config', 'promptly_cli', '.env'),
        
        # 3. Check in the home directory
        os.path.join(os.path.expanduser('~'), '.promptly_cli', '.env')
    ]
    return paths

def get_env_file_path():
    """Get the path to the .env file that exists, or return the default path"""
    for path in get_env_file_paths():
        if os.path.exists(path):
            return path
    
    # Default to the config directory
    return os.path.join(os.path.expanduser('~'), '.config', 'promptly_cli', '.env')

# Get the active .env file path
ENV_FILE_PATH = get_env_file_path()

def load_environment(force_reload=True):
    """
    Load environment variables from .env file using absolute path
    
    Args:
        force_reload (bool): Whether to force reload environment variables
    
    Returns:
        bool: True if environment was loaded successfully
    """
    # Clear any cached environment variables
    if force_reload:
        # Clear relevant environment variables to ensure fresh loading
        for key in list(os.environ.keys()):
            if key.endswith('_API_KEY') or key == 'OLLAMA_ADDR':
                os.environ.pop(key, None)
    
    # Check if .env exists
    if not os.path.exists(ENV_FILE_PATH):
        console.print(f"[yellow]Warning: Environment file not found at {ENV_FILE_PATH}[/yellow]")
        console.print("[yellow]Using default environment variables[/yellow]")
        return False
    
    # Load environment variables from file
    # Setting override=True ensures values are updated
    load_dotenv(dotenv_path=ENV_FILE_PATH, override=True)
    
    # Debug: print loaded environment variables
    #console.print(f"[green]Environment loaded from: {ENV_FILE_PATH}[/green]")
    return True

def get_api_key(provider):
    """Get API key for the specified provider"""
    # Ollama doesn't use an API key, so handle it separately
    if provider.lower() == "ollama":
        # For Ollama, we check if the address is configured
        return check_ollama_configured()
    
    env_var_name = f"{provider.upper()}_API_KEY"
    
    # Always get directly from os.environ for freshest value
    api_key = os.environ.get(env_var_name)
    
    if not api_key:
        console.print(f"[red]Error: {env_var_name} not found in environment variables[/red]")
        console.print(f"[red]Please set it in your config file: {ENV_FILE_PATH}[/red]")
        return None
    
    return api_key

def get_ollama_addr():
    """Get the address of the Ollama server"""
    ollama_addr = os.environ.get("OLLAMA_ADDR", "http://localhost:11434")
    return ollama_addr

def check_ollama_configured():
    """Check if Ollama is configured properly"""
    # Ollama typically runs on localhost:11434 by default
    # Even if OLLAMA_ADDR is not set, we can still use the default
    # Return True to indicate Ollama can potentially be used
    return True

def get_available_providers():
    """Return a list of providers that have API keys configured"""
    providers = ["openai", "mistral", "anthropic", "deepseek", "gemini", "ollama"]
    available = []
    
    for provider in providers:
        if get_api_key(provider):
            available.append(provider)
    
    return available

def debug_env_vars():
    """Debug function to print all API key environment variables and Ollama address"""
    console.print("[bold]Current Environment Variables:[/bold]")
    
    # Print API keys with masking
    for key in os.environ:
        if key.endswith('_API_KEY'):
            # Mask the actual value for security
            value = os.environ[key]
            masked_value = value[:4] + '*' * (len(value) - 4) if len(value) > 4 else '*' * len(value)
            console.print(f"  [cyan]{key}[/cyan]: {masked_value}")
    
    # Print Ollama address
    ollama_addr = get_ollama_addr()
    console.print(f"  [cyan]OLLAMA_ADDR[/cyan]: {ollama_addr}")
