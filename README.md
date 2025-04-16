# Promptly CLI

A unified command-line interface for interacting with various AI language models, including Ollama, OpenAI, Anthropic, Google Gemini, and DeepSeek.

## Features

- Single command interface for all AI providers
- Compatible with the Ollama CLI syntax
- Interactive chat mode
- Support for one-off queries
- Easy switching between providers and models
- Environment variable based configuration

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Install from source

1. Clone the repository:
```bash
git clone https://github.com/yourusername/promptly_cli.git
cd promptly_cli
```

2. Install the package:
```bash
pip install -e .
```

This will install the `llm` command globally on your system.

## Configuration

Create a `.env` file in the project root with your API keys:

```
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-...
GEMINI_API_KEY=...
DEEPSEEK_API_KEY=...
```

## Usage

### One-off queries

```bash
# Get a single response from a specific model
llm run openai/gpt-4 "What is the capital of France?"
llm run anthropic/claude-3-opus-20240229 "Explain quantum computing"
llm run ollama/llama2 "Write a short poem about coding"
```

### Interactive chat mode

```bash
# Start an interactive chat with a specific model
llm run openai/gpt-4
llm run anthropic/claude-3-sonnet-20240229
llm run ollama/mistral
```

### General shell

```bash
# Start the general shell
llm
```

### List available models

```bash
llm list
```

## Shell Commands

When in the general shell, you can use these commands:

- `help` - Display help message
- `use <provider/model>` - Switch to a specific provider and model
- `list` - List available models from all providers
- `status` - Show the status of all providers
- `clear` - Clear the terminal
- `exit` - Exit the application

When in chat mode with a specific model, you can use:

- Type your message directly to chat with the model
- `:help` - Display help message
- `:exit` - Exit chat mode
- `:clear` - Clear the terminal
- `:use <provider/model>` - Switch to a different provider/model
- `:list` - List available models
- `:reset` - Reset the chat history
- `:status` - Show the status of providers

## Examples

```bash
# Start a chat with GPT-4
llm run openai/gpt-4

# Ask a one-off question to Claude
llm run anthropic/claude-3-haiku-20240307 "What's the weather like today in Paris?"

# List all available models
llm list
```

## Project Structure

- `srcs/` - Source code
  - `main.py` - Entry point
  - `files/` - Module files
    - `providers.py` - Provider implementations
    - `shell.py` - Interactive shell
    - `status.py` - Status reporting
    - `console_config.py` - Console configuration

## Development

### Setup development environment

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
make install
```

### Run the application in development mode

```bash
make run
```

