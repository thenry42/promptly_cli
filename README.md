# Promptly CLI

A command-line interface for interacting with various AI language models.

## Current Status

This project is in early development. Currently, it provides a basic framework for a command-line tool that will eventually support multiple AI providers.

## Features (Planned)

- Single command interface for all AI providers
- Compatible with the Ollama CLI syntax
- Interactive chat mode
- Support for one-off queries
- Easy switching between providers and models
- Environment variable based configuration

## Installation

### Prerequisites

- Python 3.8 or higher
- make (for using the Makefile)

### Setup Development Environment

1. Clone the repository:
```bash
git clone https://github.com/thenry42/promptly_cli.git
cd promptly_cli
```

2. Set up the environment:
```bash
make setup
```

This will create a virtual environment and install the required dependencies.

### Setting Up API Keys

To use the tool with various AI models, you'll need to add API keys to the configuration file.

#### Option 1: During Installation

When you run the installation script, it will automatically create a configuration file and offer to open it for you to add your API keys.

#### Option 2: Using the Setup Script

You can run the setup script at any time to create or update your API keys:

```bash
./setup_keys.sh
```

#### Option 3: Manually Edit the Configuration File

The configuration file is located at:
```
~/.config/promptly_cli/.env
```

Add your API keys to this file in the following format:

```
OPENAI_API_KEY=your_openai_key_here
MISTRAL_API_KEY=your_mistral_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
GEMINI_API_KEY=your_gemini_key_here
DEEPSEEK_API_KEY=your_deepseek_key_here
OLLAMA_ADDR=http://localhost:11434
```

You can obtain API keys from:
- OpenAI (GPT models): https://platform.openai.com/api-keys
- Mistral: https://console.mistral.ai/api-keys/
- Anthropic (Claude): https://console.anthropic.com/keys
- Google (Gemini): https://ai.google.dev/tutorials/setup
- Ollama (local models): Install from https://ollama.ai

## Usage

Currently, the tool provides a simple command-line interface:

```bash
# Run without arguments (displays help)
llm

# List available models
llm list

# Start a chat with a specific model
llm run MODEL_NAME

# Get help
llm help
```

### Creating an Executable

You can create a standalone executable with:

```bash
make exe
```

This will create an executable file in the `dist/` directory that you can run directly without Python installed.

## Development

### Available Make Commands

- `make setup` - Create virtual environment and install dependencies
- `make run` - Run the application with no arguments
- `make runwith ARGS="arg1 arg2"` - Run with specific arguments
- `make test` - Run the test suite (when tests are added)
- `make exe` - Create standalone executable
- `make clean` - Remove temporary files and build artifacts
- `make help` - Display help information

## Project Structure

- `srcs/` - Source code
  - `main.py` - Entry point
  - `requirements.txt` - Project dependencies

## Roadmap

- Add support for multiple AI providers
- Implement interactive chat mode
- Create provider-specific adapters
- Add configuration management
- Publish to PyPI for easier installation

