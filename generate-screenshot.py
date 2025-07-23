#!/usr/bin/env python3
# ABOUTME: Generate sample output for README documentation
# ABOUTME: Creates text representation of the banner without external dependencies

import datetime

def generate_sample():
    """Generate a sample banner output for documentation."""
    
    # Sample ASCII art
    ascii_art = """     _   _      _ _         _____  _____ _   _ 
    | | | |    | | |       |__  / / ____| | | |
    | |_| | ___| | | ___      / / | (___ | |_| |
    |  _  |/ _ \ | |/ _ \    / /   \___ \|  _  |
    | | | |  __/ | | (_) |  / /__  ____) | | | |
    |_| |_|\___|_|_|\___/  /_____|_____/|_| |_|"""
    
    # Current date
    now = datetime.datetime.now()
    date_str = now.strftime("%A, %B %d, %Y")
    
    # Sample output
    output = f"""{ascii_art}

    Welcome back, Wils!                    System Information
    {date_str:<34} ├─ OS: Linux
    Berkeley, CA: ☀️  75°F                ├─ CPU: 45%
                                          ├─ RAM: 8.2/16.0 GB
    "Talk is cheap.                       ├─ Disk: 125.4/512.0 GB
    Show me the code."                    └─ Uptime: 2d 14h 35m
    - Linus Torvalds"""
    
    return output

if __name__ == "__main__":
    print(generate_sample())