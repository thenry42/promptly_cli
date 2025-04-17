#!/bin/bash

# Promptly CLI Installation Script

set -e  # Exit immediately if a command exits with a non-zero status

echo "=== Promptly CLI Installation ==="
echo "This script will install Promptly CLI on your system."

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for Python 3.8+
if ! command_exists python3; then
    echo "Error: Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
    echo "Error: Python 3.8+ is required. Found: $PYTHON_VERSION"
    exit 1
fi

echo "Python $PYTHON_VERSION detected."

# Check for pip
if ! command_exists pip3; then
    echo "Error: pip3 is not installed. Please install pip for Python 3."
    exit 1
fi

# Installation directory
INSTALL_DIR="$HOME/.promptly_cli"
BIN_DIR="$HOME/.local/bin"
CONFIG_DIR="$HOME/.config/promptly_cli"

# Create installation directory
echo "Creating installation directory..."
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"
mkdir -p "$CONFIG_DIR"

# Copy files
echo "Copying project files..."
cp -r ./srcs "$INSTALL_DIR/"

# Handle environment configuration
echo "Setting up configuration..."
if [ -f ".env" ]; then
    # If .env exists in current directory, copy it to config directory
    cp .env "$CONFIG_DIR/.env"
    echo "Existing .env file copied to $CONFIG_DIR/.env"
else
    # Create a template .env file if none exists
    cat > "$CONFIG_DIR/.env" << EOL
# Promptly CLI Configuration
# Add your API keys below (remove the # and add your key)

# OpenAI API key
#OPENAI_API_KEY=your_key_here

# Mistral API key
#MISTRAL_API_KEY=your_key_here

# DeepSeek API key
#DEEPSEEK_API_KEY=your_key_here

# Anthropic API key
#ANTHROPIC_API_KEY=your_key_here

# Gemini API key
#GEMINI_API_KEY=your_key_here

# Ollama address (default is localhost:11434)
OLLAMA_ADDR=http://localhost:11434
EOL
    echo "Created template .env file at $CONFIG_DIR/.env"
    echo "Please edit this file to add your API keys"
fi

# Create a symlink from the config file to the installation directory
ln -sf "$CONFIG_DIR/.env" "$INSTALL_DIR/.env"

# Create virtual environment and install dependencies
echo "Setting up virtual environment and installing dependencies..."
python3 -m venv "$INSTALL_DIR/venv"
"$INSTALL_DIR/venv/bin/pip" install --upgrade pip
"$INSTALL_DIR/venv/bin/pip" install -r "$INSTALL_DIR/srcs/requirements.txt"

# Create executable
echo "Creating executable..."
"$INSTALL_DIR/venv/bin/pip" install pyinstaller
cd "$INSTALL_DIR"
"$INSTALL_DIR/venv/bin/pyinstaller" --onefile --name llm "$INSTALL_DIR/srcs/main.py"

# Create symbolic link
echo "Creating symbolic link..."
ln -sf "$INSTALL_DIR/dist/llm" "$BIN_DIR/llm"

# Add to PATH if not already there
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo "Adding $BIN_DIR to PATH..."
    
    # Determine shell configuration file
    SHELL_CONFIG=""
    if [[ "$SHELL" == */zsh ]]; then
        SHELL_CONFIG="$HOME/.zshrc"
    elif [[ "$SHELL" == */bash ]]; then
        SHELL_CONFIG="$HOME/.bashrc"
    fi
    
    if [[ -n "$SHELL_CONFIG" ]]; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_CONFIG"
        echo "Added $BIN_DIR to your PATH in $SHELL_CONFIG"
        echo "Please run 'source $SHELL_CONFIG' to update your current session."
    else
        echo "Please manually add $BIN_DIR to your PATH."
    fi
fi

# Offer to open the config file for editing
echo ""
echo "Would you like to add your API keys now? (Recommended)"
read -p "Open the configuration file for editing? [Y/n] " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    # Try to open with the most appropriate editor
    if command_exists nano; then
        nano "$CONFIG_DIR/.env"
    elif command_exists vim; then
        vim "$CONFIG_DIR/.env"
    elif command_exists vi; then
        vi "$CONFIG_DIR/.env"
    else
        echo "No suitable text editor found. Please edit the file manually:"
        echo "$CONFIG_DIR/.env"
    fi
fi

echo ""
echo "=== Installation Complete ==="
echo "Promptly CLI has been installed successfully!"
echo "You can run it using the 'llm' command."
echo "If the command is not found, ensure $BIN_DIR is in your PATH or restart your terminal."
echo ""
echo "Your configuration file is located at: $CONFIG_DIR/.env"
echo "To add or update API keys later, edit this file."
echo ""
echo "Quick start:"
echo "  llm list            - Show available models"
echo "  llm run MODEL       - Start a chat with a specific model"
echo "  llm help            - Show more options"
echo "" 