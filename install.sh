#!/bin/bash
# ABOUTME: Install script for hello-zsh - creates symlink to script and manages config
# ABOUTME: Handles both standard installation and development setup

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo -e "${GREEN}Installing hello-zsh...${NC}"

# Check if this is a dev installation
DEV_MODE=false
if [[ "$1" == "--dev" ]]; then
    DEV_MODE=true
    echo -e "${YELLOW}Development mode installation${NC}"
fi

# Check Python 3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is required but not installed.${NC}"
    echo "Please install Python 3.8 or higher."
    exit 1
fi

# Create ~/.local/bin if it doesn't exist
if [ ! -d "$HOME/.local/bin" ]; then
    echo "Creating ~/.local/bin directory..."
    mkdir -p "$HOME/.local/bin"
fi

# Create ~/.config/hello-zsh if it doesn't exist
if [ ! -d "$HOME/.config/hello-zsh" ]; then
    echo "Creating ~/.config/hello-zsh directory..."
    mkdir -p "$HOME/.config/hello-zsh"
fi

# Create symlink to script
echo "Creating symlink for hello-zsh command..."
ln -sf "$SCRIPT_DIR/hello-zsh.py" "$HOME/.local/bin/hello-zsh"

# Handle config file
CONFIG_EXISTS=false
if [ -f "$HOME/.config/hello-zsh/config.toml" ]; then
    echo -e "${YELLOW}Config file already exists at ~/.config/hello-zsh/config.toml${NC}"
    CONFIG_EXISTS=true
else
    if [ "$DEV_MODE" = true ]; then
        # For dev mode, copy the example config (not symlink)
        echo "Copying config.toml.example for development..."
        cp "$SCRIPT_DIR/config.toml.example" "$HOME/.config/hello-zsh/config.toml"
    else
        # For normal installation, copy the example config
        echo "Creating config file..."
        cp "$SCRIPT_DIR/config.toml.example" "$HOME/.config/hello-zsh/config.toml"
    fi
fi

# Note: User configuration happens on first run of hello-zsh

# Check Python dependencies
echo -e "\n${YELLOW}Checking Python dependencies...${NC}"
MISSING_DEPS=()

# Check each dependency
python3 -c "import rich" 2>/dev/null || MISSING_DEPS+=("rich")
python3 -c "import rich_gradient" 2>/dev/null || MISSING_DEPS+=("rich-gradient")
python3 -c "import pyfiglet" 2>/dev/null || MISSING_DEPS+=("pyfiglet")
python3 -c "import requests" 2>/dev/null || MISSING_DEPS+=("requests")
python3 -c "import psutil" 2>/dev/null || MISSING_DEPS+=("psutil")

if [ ${#MISSING_DEPS[@]} -eq 0 ]; then
    echo -e "${GREEN}All Python dependencies are installed!${NC}"
else
    echo -e "${YELLOW}Missing dependencies: ${MISSING_DEPS[*]}${NC}"
    echo -e "\nTo install all dependencies at once:"
    echo -e "${GREEN}pip3 install --user rich rich-gradient pyfiglet requests psutil${NC}"
    echo -e "\nOr install using requirements.txt:"
    echo -e "${GREEN}pip3 install --user -r $SCRIPT_DIR/requirements.txt${NC}"
fi

# Check if ~/.local/bin is in PATH
PATH_OK=true
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    PATH_OK=false
    echo -e "\n${YELLOW}⚠️  WARNING: ~/.local/bin is not in your PATH${NC}"
    echo "Add this line to your ~/.zshrc or ~/.bashrc:"
    echo -e "${GREEN}export PATH=\"\$HOME/.local/bin:\$PATH\"${NC}"
    echo "Then reload your shell with: source ~/.zshrc"
fi

echo -e "\n${GREEN}✅ Installation complete!${NC}"

if [ "$DEV_MODE" = true ]; then
    echo -e "\n${YELLOW}Development setup:${NC}"
    echo "  📁 Script: $SCRIPT_DIR/hello-zsh.py"
    echo "  ⚙️  Config: ~/.config/hello-zsh/config.toml"
    echo "  🔗 Binary: ~/.local/bin/hello-zsh -> $SCRIPT_DIR/hello-zsh.py"
    echo ""
    echo "For easy config editing, create a symlink:"
    echo -e "${GREEN}ln -sf ~/.config/hello-zsh/config.toml .claude/symlinks/config.toml${NC}"
else
    echo -e "\n${GREEN}Configuration:${NC}"
    echo "  📁 Config file: ~/.config/hello-zsh/config.toml"
    echo "  ✏️  Edit config to:"
    echo "     • Change your name"
    echo "     • Customize fonts"
    echo "     • Disable weather or quotes"
    echo "     • Switch themes"
fi

echo -e "\n${GREEN}Usage:${NC}"
if [ "$PATH_OK" = true ]; then
    echo "  🚀 Test it now: hello-zsh"
else
    echo "  🚀 Test it now: $HOME/.local/bin/hello-zsh"
fi
echo "  🐚 Add to shell startup: echo 'hello-zsh' >> ~/.zshrc"
echo "  📖 Documentation: https://github.com/YOUR_USERNAME/hello-zsh"

# Show what's missing
if [ ${#MISSING_DEPS[@]} -gt 0 ] || [ "$PATH_OK" = false ]; then
    echo -e "\n${YELLOW}⚠️  Action required:${NC}"
    if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
        echo "  1. Install Python dependencies (see above)"
    fi
    if [ "$PATH_OK" = false ]; then
        echo "  2. Add ~/.local/bin to PATH (see above)"
    fi
else
    # Everything is ready - offer to test
    echo -e "\n${GREEN}Everything is ready! Would you like to see hello-zsh in action?${NC}"
    echo -n "Run hello-zsh now? [Y/n]: "
    read -n 1 RUN_NOW
    echo
    if [[ "$RUN_NOW" =~ ^[Yy]?$ ]]; then
        echo
        "$HOME/.local/bin/hello-zsh"
    fi
fi