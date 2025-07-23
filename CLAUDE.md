# CLAUDE.md

**FOLLOW ALL GLOBAL RULES UNLESS CONTRADICTED BY THIS FILE**

## Project Overview
Hello-zsh is a Tokyo Night themed terminal welcome banner with gradient text, system info, weather, and git status display.

## Project Structure
```
hello-zsh/
├── .claude/
│   ├── planning/         # Planning artifacts
│   ├── reference/        # Research & analysis
│   ├── symlinks/         # Project symlinks
│   ├── changes.md        # All change tracking
│   └── journal.md        # Technical insights & decisions
├── logs/                 # Runtime logs
├── hello-zsh.py          # Main script
├── config.toml           # Configuration file
├── requirements.txt      # Python dependencies
├── generate-*.py         # Font generation scripts
├── CHANGELOG.md          # Project changes
└── CLAUDE.md             # This file
```

## Tech Stack
- **Type**: Terminal welcome banner
- **Language**: Python 3
- **Key Libraries**: Rich (terminal rendering), pyfiglet (ASCII art), requests (weather API)
- **Dependencies**: See requirements.txt

## Code Style Notes
- Python: PEP 8 + Black formatting
- Import order: stdlib → third-party → local
- Type hints where beneficial
- Docstrings for public functions

## Core Architecture

### What We're Building
1. **Banner Display**: ASCII art with gradient colors using Tokyo Night theme
2. **System Info**: CPU, memory, disk usage with visual indicators
3. **Weather Integration**: Current weather from API
4. **Git Status**: Repository information if in git directory
5. **Configuration**: TOML-based settings for themes and fonts

## Key Files
- `hello-zsh.py` - Main script with banner generation
- `config.toml` - Theme and font configuration
- `generate-font-samples.py` - Font preview generator
- `.claude/changes.md` - All change tracking (update after every change)
- `.claude/journal.md` - Technical insights & decisions

## Testing Notes
- Test with different terminal sizes
- Verify color output in various terminals
- Check API fallbacks when offline
- Validate git status in non-git directories

## Special Notes
- **Performance**: Uses concurrent futures for parallel data fetching
- **Theming**: Tokyo Night color scheme with gradient support
- **Fonts**: Multiple ASCII art fonts with configuration

## Remember
- Keep startup time fast (<200ms ideal)
- Handle missing dependencies gracefully
- Support both light and dark terminals
- Maintain clean output formatting