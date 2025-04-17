#!/bin/bash

# Promptly CLI API Key Setup Script

echo "=== Promptly CLI API Key Setup ==="
echo "This script will help you set up your API keys for Promptly CLI."

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Configuration directory
CONFIG_DIR="$HOME/.config/promptly_cli"

# Create configuration directory if it doesn't exist
if [ ! -d "$CONFIG_DIR" ]; then
    echo "Creating configuration directory..."
    mkdir -p "$CONFIG_DIR"
fi

# Check if config file exists; if not, create a template
if [ ! -f "$CONFIG_DIR/.env" ]; then
    echo "Creating new configuration file..."
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
    echo "Created template configuration file at $CONFIG_DIR/.env"
else
    echo "Configuration file already exists at $CONFIG_DIR/.env"
fi

# Option to open the editor
echo ""
echo "Would you like to edit your API keys now?"
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
echo "=== API Key Setup Complete ==="
echo "Your configuration file is located at: $CONFIG_DIR/.env"
echo ""
echo "You can edit this file any time to update your API keys."
echo "To obtain API keys, visit the following websites:"
echo "  - OpenAI (GPT models): https://platform.openai.com/api-keys"
echo "  - Mistral: https://console.mistral.ai/api-keys/"
echo "  - Anthropic (Claude): https://console.anthropic.com/keys"
echo "  - Google (Gemini): https://ai.google.dev/tutorials/setup"
echo "  - Ollama (local models): Install from https://ollama.ai"
echo ""
echo "For more information, visit the project documentation."
echo "" 