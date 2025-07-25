#!/usr/bin/env zsh
# ABOUTME: ZSH plugin wrapper for hello-zsh - Terminal welcome banner
# ABOUTME: Supports Zinit, Oh My Zsh, and other plugin managers

# Get the plugin directory
HELLO_ZSH_DIR="${0:A:h}"

# Function to run hello-zsh
hello-zsh() {
    python3 "${HELLO_ZSH_DIR}/hello-zsh.py" "$@"
}

# Setup function for first-time users
hello-zsh-setup() {
    echo "Setting up hello-zsh..."
    
    # Create config directory
    [[ ! -d ~/.config/hello-zsh ]] && mkdir -p ~/.config/hello-zsh
    
    # Copy config if it doesn't exist
    if [[ ! -f ~/.config/hello-zsh/config.toml ]]; then
        cp "${HELLO_ZSH_DIR}/config.toml.example" ~/.config/hello-zsh/config.toml
        
        echo "Created config file at ~/.config/hello-zsh/config.toml"
        echo "Edit it to customize your name, fonts, and features!"
    fi
}

# Check dependencies on first load
hello-zsh-check-deps() {
    local missing_deps=()
    
    python3 -c "import rich" 2>/dev/null || missing_deps+=("rich")
    python3 -c "import rich_gradient" 2>/dev/null || missing_deps+=("rich-gradient")
    python3 -c "import pyfiglet" 2>/dev/null || missing_deps+=("pyfiglet")
    python3 -c "import requests" 2>/dev/null || missing_deps+=("requests")
    python3 -c "import psutil" 2>/dev/null || missing_deps+=("psutil")
    
    if [[ ${#missing_deps[@]} -gt 0 ]]; then
        echo "hello-zsh: Missing Python dependencies: ${missing_deps[*]}"
        echo "Install with: pip3 install --user ${missing_deps[*]}"
        return 1
    fi
    return 0
}

# Initialize on first run
if [[ ! -f ~/.config/hello-zsh/config.toml ]]; then
    hello-zsh-setup
fi

# Environment variable to disable auto-run
: ${HELLO_ZSH_AUTO:=true}

# Auto-run on interactive shell startup (if enabled and deps are met)
if [[ -o interactive ]] && [[ "$HELLO_ZSH_AUTO" == "true" ]]; then
    if hello-zsh-check-deps 2>/dev/null; then
        hello-zsh
    fi
fi

# For completeness, export the function
export -f hello-zsh 2>/dev/null || true