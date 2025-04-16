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
git clone https://github.com/yourusername/promptly_cli.git
cd promptly_cli
```

2. Set up the environment:
```bash
make setup
```

This will create a virtual environment and install the required dependencies.

## Usage

Currently, the tool provides a simple command-line interface:

```bash
# Run without arguments (displays "Hello, world!")
make run

# Run with arguments
make runwith ARGS="arg1 arg2 arg3"
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

