#!/bin/bash

# Promptly CLI Uninstallation Script

echo "=== Promptly CLI Uninstallation ==="
echo "This script will remove Promptly CLI from your system."
echo "Note: This will not remove any entries added to your shell configuration files."

# Installation directories
INSTALL_DIR="$HOME/.promptly_cli"
BIN_DIR="$HOME/.local/bin"
CONFIG_DIR="$HOME/.config/promptly_cli"
CONFIG_FILE="$CONFIG_DIR/.env"
EXECUTABLE="$BIN_DIR/llm"

# Confirm uninstallation
read -p "Are you sure you want to uninstall Promptly CLI? [y/N] " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Uninstallation cancelled."
    exit 0
fi

# Ask about preserving configuration
PRESERVE_CONFIG=false
read -p "Do you want to keep your API keys and configuration in $CONFIG_FILE? [Y/n] " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    PRESERVE_CONFIG=true
    echo "Configuration and API keys will be preserved at $CONFIG_DIR"
else
    echo "Configuration directory including API keys will be removed"
fi

# Remove symbolic link
echo "Removing symbolic link..."
if [ -L "$EXECUTABLE" ]; then
    rm "$EXECUTABLE"
    echo "Symbolic link removed."
else
    echo "No symbolic link found at $EXECUTABLE."
fi

# Remove installation directory
echo "Removing installation directory..."
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "Installation directory removed."
else
    echo "No installation directory found at $INSTALL_DIR."
fi

# Remove configuration directory (if requested)
if [ "$PRESERVE_CONFIG" = false ]; then
    echo "Removing API key configuration directory..."
    if [ -d "$CONFIG_DIR" ]; then
        rm -rf "$CONFIG_DIR"
        echo "Configuration directory and API keys removed."
    else
        echo "No configuration directory found at $CONFIG_DIR."
    fi
fi

echo ""
echo "=== Uninstallation Complete ==="
echo "Promptly CLI has been uninstalled."
echo ""
if [ "$PRESERVE_CONFIG" = true ]; then
    echo "Your API keys and configuration have been preserved at $CONFIG_FILE"
    echo "You can remove them manually later if needed with:"
    echo "  rm -rf $CONFIG_DIR"
fi
echo ""
echo "If you added $BIN_DIR to your PATH manually, you may want to remove it."
echo "Check your shell configuration files (~/.bashrc, ~/.zshrc, etc.) for any lines that were added."
echo "" 