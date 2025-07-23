#!/usr/bin/env python3
# ABOUTME: Rich-based Tokyo Night themed terminal welcome banner with gradient text
# ABOUTME: Features system info, weather, git status in beautiful column layout

import os
import sys
import subprocess
import datetime
import json
import time
import tomllib
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from rich.columns import Columns
from rich.align import Align
from rich.table import Table
from rich_gradient import Gradient
from rich.style import Style
from rich.box import ROUNDED, Box
import pyfiglet

# Load configuration
def load_config():
    """Load configuration from config.toml"""
    config_path = Path(__file__).parent / 'config.toml'
    
    # Default config if file doesn't exist
    default_config = {
        'theme': 'tokyo-night',
        'ascii_fonts': ['poison', 'larry3d', 'graffiti', 'modular', 'colossal'],
        'themes': {
            'tokyo-night': {
                'red': '#f7768e',
                'orange': '#ff9e64',
                'yellow': '#e0af68',
                'green': '#9ece6a',
                'teal': '#73daca',
                'cyan': '#7dcfff',
                'blue': '#7aa2f7',
                'purple': '#bb9af7',
                'white': '#c0caf5',
                'foreground': '#a9b1d6',
                'text': '#9aa5ce',
                'dim': '#565f89',
                'black': '#414868',
                'background': '#1a1b26'
            }
        }
    }
    
    try:
        with open(config_path, 'rb') as f:
            config = tomllib.load(f)
            return config
    except FileNotFoundError:
        return default_config
    except Exception as e:
        print(f"Error loading config: {e}")
        return default_config

# Load config and set theme
CONFIG = load_config()
ACTIVE_THEME = CONFIG.get('theme', 'tokyo-night')
THEME = CONFIG['themes'][ACTIVE_THEME]
ASCII_FONTS = CONFIG.get('ascii_fonts', ['poison', 'larry3d', 'graffiti'])

# Create a box style with no borders
NO_BORDER = Box(
    """\
    
    
    
    
    
    
    
    
"""
)

# Cache settings
CACHE_DIR = Path.home() / '.cache' / 'welcome-banner'
WEATHER_CACHE_FILE = CACHE_DIR / 'weather.json'
CACHE_DURATION = 300  # 5 minutes

def ensure_cache_dir():
    """Create cache directory if it doesn't exist"""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

def get_greeting():
    """Get time-based greeting with ASCII art and gradient colors"""
    hour = datetime.datetime.now().hour
    
    if hour < 4 or hour > 22:
        greeting = "Good Night!"
        short_greeting = "NIGHT"
        colors = [THEME['purple'], THEME['blue'], THEME['dim']]
    elif hour < 12:
        greeting = "Good Morning!"
        short_greeting = "MORNING"
        colors = [THEME['blue'], THEME.get('light_cyan', THEME['cyan']), THEME['white']]
    elif hour < 17:
        greeting = "Good Afternoon!"
        short_greeting = "AFTERNOON"
        colors = [THEME['yellow'], THEME['orange'], THEME['white']]
    else:
        greeting = "Good Evening!"
        short_greeting = "EVENING"
        colors = [THEME['purple'], THEME['blue'], THEME['dim']]
    
    # Get terminal width for responsive greeting text
    import shutil
    terminal_width, _ = shutil.get_terminal_size()
    
    # Rotate between fonts randomly from config
    import random
    selected_font = random.choice(ASCII_FONTS)
    
    # For very narrow terminals, use shorter greeting
    if terminal_width < 60:
        display_greeting = short_greeting
    else:
        display_greeting = greeting
    
    # Create ASCII art using pyfiglet with terminal width
    try:
        ascii_art = pyfiglet.figlet_format(display_greeting, font=selected_font, width=terminal_width)
    except Exception:
        # Fallback to a simple font if the selected one fails
        ascii_art = pyfiglet.figlet_format(display_greeting, font='standard', width=terminal_width)
    
    # Apply gradient to ASCII art
    gradient_text = Gradient(ascii_art.rstrip(), colors=colors)
    
    # Return gradient text without centering - we'll center it when printing
    return gradient_text

def run_command(cmd, timeout=1.0):
    """Run shell command with timeout"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except subprocess.TimeoutExpired:
        return None
    except Exception:
        return None

def get_system_info():
    """Get system information"""
    info = []
    
    # OS info - more compact
    os_info = run_command("uname -s")
    kernel = run_command("uname -r | cut -d'-' -f1")
    if os_info and kernel:
        info.append(f"[{THEME['dim']}]OS:[/] {os_info} {kernel}")
    
    # Hostname
    hostname = run_command("hostname")
    if hostname:
        info.append(f"[{THEME['dim']}]Host:[/] {hostname}")
    
    # Shell
    shell = os.environ.get('SHELL', 'unknown').split('/')[-1]
    zsh_version = run_command("zsh --version | awk '{print $2}'")
    if zsh_version:
        info.append(f"[{THEME['dim']}]Shell:[/] {shell} {zsh_version}")
    else:
        info.append(f"[{THEME['dim']}]Shell:[/] {shell}")
    
    # Memory - more compact
    mem_info = run_command("free -h | awk '/^Mem:/ {print $3 \"/\" $2}'")
    if mem_info:
        info.append(f"[{THEME['dim']}]Mem:[/] {mem_info}")
    
    # Uptime - simplified
    uptime = run_command("uptime -p | sed 's/up //' | sed 's/ hours/, /g' | sed 's/ minutes/ min/g'")
    if uptime:
        info.append(f"[{THEME['dim']}]Up:[/] {uptime}")
    
    # IP Address - just last octet if too long
    ip = run_command("ip route get 1 2>/dev/null | awk '{print $7;exit}' || hostname -I 2>/dev/null | awk '{print $1}'")
    if ip and len(ip) > 12:
        # Show first 3 octets + last
        parts = ip.split('.')
        if len(parts) == 4:
            ip = f"{'.'.join(parts[:3])}.{parts[3]}"
    if ip:
        info.append(f"[{THEME['dim']}]IP:[/] {ip}")
    
    return "\n".join(info)

def get_git_info():
    """Get git repository information"""
    # Check if we're in a git repo
    if not run_command("git rev-parse --git-dir"):
        return None
    
    info = []
    
    # Branch
    branch = run_command("git branch --show-current")
    if branch:
        info.append(f"[{THEME['dim']}]Branch:[/] [{THEME['green']}]{branch}[/]")
    
    # Status
    status_count = run_command("git status --porcelain 2>/dev/null | wc -l")
    if status_count and status_count != "0":
        info.append(f"[{THEME['dim']}]Changes:[/] [{THEME['yellow']}]{status_count} files[/]")
    else:
        info.append(f"[{THEME['dim']}]Status:[/] [{THEME['green']}]Clean ✓[/]")
    
    return "\n".join(info) if info else None

def get_weather_cached():
    """Get weather with caching"""
    ensure_cache_dir()
    
    # Check cache
    if WEATHER_CACHE_FILE.exists():
        try:
            with open(WEATHER_CACHE_FILE, 'r') as f:
                cache_data = json.load(f)
                if time.time() - cache_data['timestamp'] < CACHE_DURATION:
                    return cache_data['weather']
        except:
            pass
    
    # Fetch new weather
    weather = run_command("curl -s 'https://wttr.in?format=%c+%t+%p+%h'", timeout=0.8)
    
    if weather:
        # Cache the result
        try:
            with open(WEATHER_CACHE_FILE, 'w') as f:
                json.dump({
                    'timestamp': time.time(),
                    'weather': weather
                }, f)
        except:
            pass
    
    return weather

def format_weather(weather_data):
    """Format weather data"""
    if not weather_data:
        return "[dim]No weather data[/]"
    
    parts = weather_data.split()
    if len(parts) >= 4:
        icon = parts[0]
        temp = parts[1]
        precip = parts[2]
        humidity = parts[3]
        
        info = [f"{icon} [{THEME['red']}]{temp}[/]"]
        
        if precip != "0.0mm":
            info.append(f"[{THEME['dim']}]Rain:[/] [{THEME['blue']}]{precip}[/]")
        
        info.append(f"[{THEME['dim']}]Humidity:[/] {humidity}")
        
        return "\n".join(info)
    
    return weather_data

def get_date_info():
    """Get date and time information"""
    now = datetime.datetime.now()
    
    info = [
        f"[{THEME['dim']}]Date:[/] {now.strftime('%a, %b %d')}",
        f"[{THEME['dim']}]Time:[/] {now.strftime('%I:%M %p')}"
    ]
    
    # Last login
    last_login = run_command(f"last -1 -R $USER 2>/dev/null | head -1 | awk '{{if (NF >= 7) print $3\" \"$4\" \"$5}}'")
    if last_login:
        info.append(f"[{THEME['dim']}]Last:[/] {last_login}")
    
    return "\n".join(info)

def get_random_quote():
    """Get a random programming quote"""
    quotes = [
        ("Talk is cheap. Show me the code.", "Linus Torvalds"),
        ("Premature optimization is the root of all evil.", "Donald Knuth"),
        ("Make it work, make it right, make it fast.", "Kent Beck"),
        ("Simplicity is the soul of efficiency.", "Austin Freeman"),
        ("First, solve the problem. Then, write the code.", "John Johnson"),
        ("Any fool can write code that a computer can understand. Good programmers write code that humans can understand.", "Martin Fowler"),
        ("Debugging is twice as hard as writing the code in the first place.", "Brian Kernighan"),
        ("Code is like humor. When you have to explain it, it's bad.", "Cory House"),
    ]
    
    import random
    return random.choice(quotes)

def main():
    """Main function to display the welcome banner"""
    # Get actual terminal size - try multiple methods
    import shutil
    import os
    
    # Try to get real terminal width
    term_cols = None
    
    # Method 1: tput (most reliable)
    try:
        tput_width = run_command("tput cols")
        if tput_width:
            term_cols = int(tput_width)
    except:
        pass
    
    # Method 2: stty
    if not term_cols:
        try:
            stty_size = run_command("stty size 2>/dev/null")
            if stty_size:
                _, term_cols = map(int, stty_size.split())
        except:
            pass
    
    # Method 3: shutil fallback
    if not term_cols:
        term_cols, _ = shutil.get_terminal_size()
    
    # Create console with explicit terminal width
    console = Console(width=term_cols, legacy_windows=False)
    
    # Get terminal width for responsive layout
    terminal_width = term_cols
    
    # Clear screen (skip in VSCode terminal for compatibility)
    if os.environ.get('TERM_PROGRAM') != 'vscode':
        console.clear()
    
    # Get all data in parallel for speed
    with ThreadPoolExecutor(max_workers=4) as executor:
        system_future = executor.submit(get_system_info)
        git_future = executor.submit(get_git_info)
        weather_future = executor.submit(get_weather_cached)
        date_future = executor.submit(get_date_info)
    
    # Create gradient banner that fills the width
    banner = get_greeting()
    
    # Add top padding
    console.print("\n")
    
    # Print banner centered
    from rich.align import Align
    centered_banner = Align(banner, align="center")
    console.print(centered_banner)
    
    # Add bottom padding
    console.print("\n")
    
    # Get data
    system_info = system_future.result()
    git_info = git_future.result()
    date_info = date_future.result()
    weather_data = weather_future.result()
    
    # Create natural language greeting with weather
    now = datetime.datetime.now()
    greeting_text = f"[bold {THEME['cyan']}]Hi Wils![/] "
    
    # Add time-based greeting with randomization
    import random
    hour = now.hour
    
    if 22 <= hour or hour < 5:  # Late Night (22:00-04:59)
        late_night_greetings = [
            "Working late tonight?",
            "Burning the midnight oil?", 
            "Late night coding session?",
            "The night owl is active!",
            "Late night productivity?"
        ]
        greeting_text += f"[{THEME['foreground']}]{random.choice(late_night_greetings)}[/] "
    elif 5 <= hour < 9:  # Early Morning (05:00-08:59)
        early_morning_greetings = [
            "Rise and grind!",
            "Early bird today!",
            "Starting the day strong!",
            "Morning energy activated!",
            "Ready to conquer the day?"
        ]
        greeting_text += f"[{THEME['foreground']}]{random.choice(early_morning_greetings)}[/] "
    elif 9 <= hour < 12:  # Morning (09:00-11:59) 
        morning_greetings = [
            "Hope your morning is going well.",
            "Good morning vibes!",
            "Morning productivity time!",
            "Starting the day right!",
            "Morning momentum building!"
        ]
        greeting_text += f"[{THEME['foreground']}]{random.choice(morning_greetings)}[/] "
    elif 12 <= hour < 17:  # Afternoon (12:00-16:59)
        afternoon_greetings = [
            "Hope your afternoon is productive!",
            "Afternoon energy flowing!",
            "Midday check-in time!",
            "Afternoon momentum going strong!",
            "Hope your day is treating you well."
        ]
        greeting_text += f"[{THEME['foreground']}]{random.choice(afternoon_greetings)}[/] "
    else:  # Evening (17:00-21:59)
        evening_greetings = [
            "Good to see you this evening!",
            "Evening productivity session?",
            "Winding down or ramping up?",
            "Evening vibes activated!",
            "Hope your evening is going well."
        ]
        greeting_text += f"[{THEME['foreground']}]{random.choice(evening_greetings)}[/] "
    
    # Add date in natural language
    greeting_text += f"[{THEME['foreground']}]It's[/] [{THEME['blue']}]{now.strftime('%A, %B %d')}[/] [{THEME['foreground']}]at[/] [{THEME['blue']}]{now.strftime('%I:%M %p')}[/]. "
    
    # Add weather in natural language
    if weather_data:
        parts = weather_data.split()
        if len(parts) >= 4:
            icon = parts[0]
            temp = parts[1]
            precip = parts[2]
            humidity = parts[3]
            
            # Get weather color mappings from config
            weather_colors = CONFIG['themes'][ACTIVE_THEME].get('weather', {})
            
            # Map weather icons to colored descriptions
            weather_descriptions = {
                '☀️': f"[{THEME.get(weather_colors.get('sunny', 'yellow'), THEME['yellow'])}]clear and sunny[/]",
                '🌤️': f"[{THEME.get(weather_colors.get('sunny', 'yellow'), THEME['yellow'])}]mostly sunny[/]",
                '⛅️': f"[{THEME.get(weather_colors.get('windy', 'white'), THEME['white'])}]partly cloudy[/]", 
                '☁️': f"[{THEME.get(weather_colors.get('cloudy', 'dim'), THEME['dim'])}]cloudy[/]",
                '🌫️': f"[{THEME.get(weather_colors.get('cloudy', 'dim'), THEME['dim'])}]foggy[/]",
                '🌧️': f"[{THEME.get(weather_colors.get('rainy', 'blue'), THEME['blue'])}]rainy[/]",
                '⛈️': f"[{THEME.get(weather_colors.get('stormy', 'purple'), THEME['purple'])}]stormy with thunderstorms[/]",
                '🌩️': f"[{THEME.get(weather_colors.get('stormy', 'purple'), THEME['purple'])}]thunderstorms[/]",
                '🌨️': f"[{THEME.get(weather_colors.get('snowy', 'light_cyan'), THEME.get('light_cyan', THEME['cyan']))}]snowy[/]",
                '❄️': f"[{THEME.get(weather_colors.get('snowy', 'light_cyan'), THEME.get('light_cyan', THEME['cyan']))}]snowing[/]",
                '🌦️': f"[{THEME.get(weather_colors.get('sunny', 'yellow'), THEME['yellow'])}]sunny[/] [{THEME['foreground']}]with some[/] [{THEME.get(weather_colors.get('rainy', 'blue'), THEME['blue'])}]rain[/]",
                '🌥️': f"[{THEME.get(weather_colors.get('cloudy', 'dim'), THEME['dim'])}]mostly cloudy[/]",
                '🌪️': f"[{THEME.get(weather_colors.get('danger', 'red'), THEME['red'])}]tornado warning[/]",
                '🌬️': f"[{THEME.get(weather_colors.get('windy', 'white'), THEME['white'])}]windy[/]"
            }
            
            # Get description or default to showing the icon
            condition = weather_descriptions.get(icon, f"showing {icon}")
            
            greeting_text += f"\n\n[{THEME['foreground']}]It's[/] {condition} [{THEME['foreground']}]outside at[/] [{THEME['cyan']}]{temp}[/]"
            
            if precip != "0.0mm":
                greeting_text += f" [{THEME['foreground']}]with[/] [{THEME['blue']}]{precip}[/] [{THEME['foreground']}]of precipitation[/]"
            
            greeting_text += f" [{THEME['foreground']}]and[/] [{THEME['cyan']}]{humidity}[/] [{THEME['foreground']}]humidity.[/]"
    
    # Add last login info
    last_login = run_command(f"last -1 -R $USER 2>/dev/null | head -1 | awk '{{if (NF >= 7) print $3\" \"$4\" \"$5}}'")
    if last_login:
        greeting_text += f"\n\n[{THEME['dim']}]Last login: {last_login}[/]"
    
    # Create system info content
    system_content = system_info
    if git_info:
        system_content += f"\n\n{git_info}"
    
    # Quote
    quote, author = get_random_quote()
    quote_text = Text()
    quote_text.append(f'"{quote}"', style=THEME["blue"])
    quote_text.append(f'\n— {author}', style=THEME["dim"])
    
    # Center the quote
    centered_quote = Align(quote_text, align="center")
    
    # Create greeting panel with no borders
    greeting_panel = Panel(
        Align(greeting_text, align="center"),
        box=NO_BORDER,  # Use custom no-border box
        padding=(1, 4),  # Same padding as system panel
        expand=False
    )
    
    # Create system panel with centered content
    centered_system_content = Align(system_content, align="center")
    system_panel = Panel(
        centered_system_content,
        title=f"[bold {THEME['blue']}]System[/]",
        title_align="center",
        border_style=THEME['black'],
        padding=(1, 4),  # Same padding as greeting text
        expand=False  # Auto-size to content
    )
    
    # Create layout based on terminal width
    if terminal_width < 80:
        # For narrow terminals, stack vertically
        console.print(greeting_panel, justify="center")
        console.print()
        console.print(system_panel, justify="center")
    else:
        # For wider terminals, use two-column layout
        from rich.table import Table
        grid = Table.grid(expand=True)
        grid.add_column(ratio=2)  # Left column
        grid.add_column(ratio=1)  # Right column
        
        # Add row with greeting panel and system panel
        # Center the greeting panel in its column
        grid.add_row(Align(greeting_panel, align="center"), system_panel)
        
        console.print(grid)
    
    # Add padding before quote
    console.print("\n")
    
    # Print centered quote
    console.print(centered_quote)
    
    # Add bottom padding
    console.print("\n")

if __name__ == "__main__":
    main()