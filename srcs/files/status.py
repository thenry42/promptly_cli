import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console

# Create a local console instance for this module
console = Console()

# Try importing provider libraries, but handle missing ones gracefully
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    console.print("Warning: ollama module not available", style="yellow")

try:
    import mistralai
    MISTRAL_AVAILABLE = True
except ImportError:
    MISTRAL_AVAILABLE = False
    console.print("Warning: mistralai module not available", style="yellow")

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    console.print("Warning: openai module not available", style="yellow")

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    console.print("Warning: anthropic module not available", style="yellow")

try:
    from google import genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    console.print("Warning: google.genai module not available", style="yellow")

# Find and load the .env file using an absolute path approach
def load_environment():
    """Load environment variables from .env file using absolute path"""
    # Get the absolute path of the current file
    current_file = os.path.abspath(__file__)
    
    # Navigate up to project root (2 levels up from current file)
    current_dir = os.path.dirname(current_file)
    srcs_dir = os.path.dirname(current_dir)
    project_root = os.path.dirname(srcs_dir)
    
    # Construct the path to the .env file
    env_path = os.path.join(project_root, '.env')
    
    # Print debug information
    console.print(f"Current working directory: {os.getcwd()}", style="cyan")
    console.print(f"Current file: {current_file}", style="cyan")
    console.print(f"Looking for .env at: {env_path}", style="cyan")
    console.print(f".env exists: {os.path.exists(env_path)}", style="cyan")
    
    # Load the environment variables
    if os.path.exists(env_path):
        console.print(f"Loading environment from: {env_path}", style="cyan")
        # Load environment variables explicitly
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value
                
        # Also try the regular load_dotenv for backup
        load_dotenv(env_path)
        
        # Verify loading
        mistral_key = os.getenv("MISTRAL_API_KEY")
        if mistral_key:
            console.print(f"Environment loaded successfully: {mistral_key[:4]}...", style="green")
        else:
            console.print("Environment loaded but variables not found", style="red")
    else:
        console.print("Environment file not found!", style="red")
        
    # Print out all environment variables for debugging
    for key in ["MISTRAL_API_KEY", "OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GEMINI_API_KEY", "DEEPSEEK_API_KEY"]:
        value = os.getenv(key)
        if value:
            # Only print first few characters for security
            console.print(f"[ENV] {key}: {value[:4]}...", style="green")
        else:
            console.print(f"[ENV] {key}: None", style="red")

# Call the environment loading function
load_environment()

def get_status() -> list[str]:
    """Get a list of available AI providers based on valid API credentials."""

    # Debug: Print environment variables to check if they're loaded correctly
    mistral_key = os.getenv("MISTRAL_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")
    deepseek_key = os.getenv("DEEPSEEK_API_KEY")
    
    print("=== API KEYS STATUS ===")
    print(f"MISTRAL_API_KEY: {mistral_key}")
    print(f"OPENAI_API_KEY: {openai_key}")
    print(f"ANTHROPIC_API_KEY: {anthropic_key}")
    print(f"GEMINI_API_KEY: {gemini_key}")
    print(f"DEEPSEEK_API_KEY: {deepseek_key}")
    
    # Check for Ollama
    if OLLAMA_AVAILABLE:
        try:
            client = ollama.Client()
            # Try to list models to verify connection
            models = client.list()
            console.print("ollama available", style="green")
        except Exception as e:
            console.print(f"ollama error: {str(e)}", style="red")
    
    # Check for Mistral
    if MISTRAL_AVAILABLE and mistral_key:
        try:
            client = mistralai.Mistral(api_key=mistral_key)
            console.print("mistral api key set", style="green")
        except Exception as e:
            console.print(f"mistral error: {str(e)}", style="red")
    
    # Check for OpenAI
    if OPENAI_AVAILABLE and openai_key:
        try:
            client = openai.OpenAI(api_key=openai_key)
            console.print("openai api key set", style="green")
        except Exception as e:
            console.print(f"openai error: {str(e)}", style="red")
    
    # Check for Anthropic
    if ANTHROPIC_AVAILABLE and anthropic_key:
        try:
            client = anthropic.Anthropic(api_key=anthropic_key)
            console.print("anthropic api key set", style="green")
        except Exception as e:
            console.print(f"anthropic error: {str(e)}", style="red")
    
    # Check for Gemini
    if GEMINI_AVAILABLE and gemini_key:
        try:
            client = genai.Client(api_key=gemini_key)
            console.print("gemini api key set", style="green")
        except Exception as e:
            console.print(f"gemini error: {str(e)}", style="red")
    
    # Check for DeepSeek (uses OpenAI's API format)
    if OPENAI_AVAILABLE and deepseek_key:
        try:
            client = openai.OpenAI(api_key=deepseek_key, base_url="https://api.deepseek.com/v1")
            console.print("deepseek api key set", style="green")
        except Exception as e:
            console.print(f"deepseek error: {str(e)}", style="red")
            
