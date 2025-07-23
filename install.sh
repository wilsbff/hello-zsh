#!/bin/bash
# ABOUTME: Install script for hello-zsh - creates symlink directly to development directory
# ABOUTME: Simple setup for development - just creates command in ~/.local/bin

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo -e "${GREEN}Installing hello-zsh...${NC}"

# Create ~/.local/bin if it doesn't exist
if [ ! -d "$HOME/.local/bin" ]; then
    echo "Creating ~/.local/bin directory..."
    mkdir -p "$HOME/.local/bin"
fi

# Create symlink
echo "Creating symlink..."
ln -sf "$SCRIPT_DIR/hello-zsh.py" "$HOME/.local/bin/hello-zsh"

# Check for Python dependencies
echo -e "\n${YELLOW}Checking Python dependencies...${NC}"
MISSING_DEPS=()

# Check each dependency
python3 -c "import rich" 2>/dev/null || MISSING_DEPS+=("rich")
python3 -c "import rich_gradient" 2>/dev/null || MISSING_DEPS+=("rich-gradient")
python3 -c "import pyfiglet" 2>/dev/null || MISSING_DEPS+=("pyfiglet")
python3 -c "import requests" 2>/dev/null || MISSING_DEPS+=("requests")
python3 -c "import psutil" 2>/dev/null || MISSING_DEPS+=("psutil")

if [ ${#MISSING_DEPS[@]} -eq 0 ]; then
    echo -e "${GREEN}All Python dependencies are already installed!${NC}"
else
    echo -e "${YELLOW}Missing dependencies: ${MISSING_DEPS[*]}${NC}"
    echo -e "\nTo install dependencies, you can use one of these methods:"
    echo "  1. Using pipx (recommended):"
    echo "     pipx install --include-deps hello-zsh"
    echo "  2. Using pip with --user flag:"
    echo "     pip3 install --user ${MISSING_DEPS[*]}"
    echo "  3. Using system packages (if available):"
    echo "     sudo apt install python3-rich python3-pyfiglet python3-requests python3-psutil"
fi

echo -e "\n${GREEN}Installation complete!${NC}"
echo -e "\n${YELLOW}Development setup:${NC}"
echo "  - Script location: $SCRIPT_DIR/hello-zsh.py"
echo "  - Config file: $SCRIPT_DIR/config.toml"
echo "  - Command symlink: ~/.local/bin/hello-zsh"

if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo -e "\n${YELLOW}Note: ~/.local/bin is not in your PATH${NC}"
    echo "Add this to your ~/.zshrc or ~/.bashrc:"
    echo '  export PATH="$HOME/.local/bin:$PATH"'
fi

echo -e "\nTo use hello-zsh:"
echo "  - Run command: hello-zsh"
echo "  - Or directly: python3 $SCRIPT_DIR/hello-zsh.py"
echo -e "\nTo add to shell startup, add this line to ~/.zshrc:"
echo "  hello-zsh"