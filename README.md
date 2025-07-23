# Hello ZSH 🌃

A beautiful terminal welcome banner for ZSH with Tokyo Night theme support, ASCII art headers, and system information display.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Features

- 🎨 **Customizable ASCII Art Headers** - Multiple font options with gradient support
- 🌃 **Tokyo Night Theme** - Beautiful dark theme with customizable colors
- 📊 **System Information** - CPU, RAM, disk usage, and uptime display
- 🌤️ **Weather Integration** - Current weather conditions for your location
- 💡 **Inspirational Quotes** - Random quotes from hacker-quotes
- 📱 **Responsive Design** - Adapts to terminal width automatically

## Installation

### Prerequisites

```bash
# Required Python packages
pip install rich pyfiglet requests psutil
```

### Quick Install

1. Clone the repository:
```bash
git clone https://github.com/yourusername/hello-zsh.git
mkdir -p ~/.config/hello-zsh
cp hello-zsh/* ~/.config/hello-zsh/
```

2. Add to your `.zshrc`:
```bash
# Tokyo Night Welcome Banner
if [[ $- == *i* ]] && [[ -f ~/.config/hello-zsh/hello-zsh.py ]]; then
    python3 -O ~/.config/hello-zsh/hello-zsh.py
fi
```

## Configuration

Edit `config.toml` to customize your banner:

```toml
# Theme selection
theme = "tokyo-night"  # or "tokyo-storm"

# ASCII fonts (randomly selected)
ascii_fonts = ["slant", "graffiti", "bloody", "doom", "larry3d"]

# Custom greeting (optional)
# greeting = "Welcome back, hacker!"
```

### Available Themes

- **tokyo-night**: Default dark theme with vibrant colors
- **tokyo-storm**: Darker variant with muted tones

### ASCII Font Options

Popular fonts include:
- `slant` - Clean and readable
- `graffiti` - Street art style
- `bloody` - Horror themed
- `doom` - Classic gaming style
- `larry3d` - 3D effect

Run `pyfiglet -l` to see all available fonts.

## Customization

### Adding Custom Themes

Add your theme to `config.toml`:

```toml
[themes.my-theme]
red = '#ff0000'
orange = '#ff8800'
yellow = '#ffff00'
green = '#00ff00'
blue = '#0088ff'
purple = '#8800ff'
cyan = '#00ffff'
fg = '#ffffff'
bg = '#000000'
selection = '#444444'
comment = '#888888'
```

### Weather Location

The banner auto-detects your location. To set manually:

```python
# In hello-zsh.py, modify the weather URL:
weather_url = "https://wttr.in/YourCity?format=%C+%t"
```

## Screenshots

<details>
<summary>Tokyo Night Theme</summary>

```
     _   _      _ _         _____  _____ _   _ 
    | | | |    | | |       |__  / / ____| | | |
    | |_| | ___| | | ___      / / | (___ | |_| |
    |  _  |/ _ \ | |/ _ \    / /   \___ \|  _  |
    | | | |  __/ | | (_) |  / /__  ____) | | | |
    |_| |_|\___|_|_|\___/  /_____|_____/|_| |_|

    Welcome back, Wils!                    System Information
    Tuesday, July 23, 2024                ├─ OS: Linux
    Berkeley, CA: ☀️  75°F                ├─ CPU: 45%
                                          ├─ RAM: 8.2/16.0 GB
    "Talk is cheap.                       ├─ Disk: 125.4/512.0 GB
    Show me the code."                    └─ Uptime: 2d 14h 35m
    - Linus Torvalds
```

</details>

## Troubleshooting

### Unicode/Emoji Issues

If borders appear misaligned, ensure your terminal supports Unicode properly. The banner avoids emoji characters by default for better compatibility.

### Terminal Width Detection

The banner auto-detects terminal width. If text appears wrapped incorrectly, try:

```bash
export COLUMNS=$(tput cols)
```

### Performance

For faster startup, run with optimization:

```bash
python3 -O ~/.config/hello-zsh/hello-zsh.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- [Rich](https://github.com/Textualize/rich) - Beautiful terminal formatting
- [PyFiglet](https://github.com/pwaller/pyfiglet) - ASCII art generation
- [Tokyo Night](https://github.com/enkia/tokyo-night-vscode-theme) - Color scheme inspiration