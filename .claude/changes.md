# Changes Log

## 2025-07-25

### Performance Optimizations
- Replaced 15+ subprocess calls with native Python libraries for significant performance improvement:
  - `platform.system()` and `platform.release()` replace `uname` commands
  - `socket.gethostname()` replaces `hostname` subprocess
  - `psutil.virtual_memory()` replaces `free` command
  - `psutil.boot_time()` for uptime calculation
- Optimized git operations to use single batched command instead of 3-4 separate calls
- Added 2-second timeout to weather API call with `curl -m 2`
- Increased weather cache duration from 5 minutes to 30 minutes
- Simplified terminal width detection to use `os.get_terminal_size()` with `shutil` fallback
- Fixed unused imports and variables (removed duplicate Align import, unused date_info)

### Performance Impact
- Estimated reduction in startup time from ~500ms to <100ms
- Subprocess calls reduced from 15+ to ~3 (zsh version, IP address, git batch)
- Weather API no longer blocks startup beyond 2 seconds

## 2025-01-24

### Fixed Duplicate Banner Execution
- Identified issue: both old welcome-banner.py and new hello-zsh were running
- Old banner was at ~/.config/welcome-banner/welcome-banner.py (called from ~/.zshrc:153-156)
- Commented out old welcome-banner code block in ~/.zshrc
- Only hello-zsh now runs on terminal startup

### Fixed Docker Completions Error
- Removed broken Docker completions symlink at /usr/share/zsh/vendor-completions/_docker
- Symlink was pointing to non-existent Docker Desktop path in WSL
- Error "compinit:527: no such file or directory" no longer appears on startup

### Updated Font Sample Generation
- Changed default text from "Wils"/"Test" to "Good Afternoon" in generate-font-samples.py
- Updated current-fonts-samples.py to match config.toml fonts (slant, alligator2, graffiti, bloody, larry3d)
- Regenerated both font-samples.txt (550 fonts) and current-fonts-samples.txt (5 fonts)

### Fixed Config Loading Issue
- Config wasn't loading due to symlink resolution
- Fixed by using Path(__file__).resolve().parent in load_config()
- Now correctly loads all fonts from config.toml

### Restructured Configuration Management
- Moved to XDG-compliant config location: ~/.config/hello-zsh/config.toml
- Renamed config.toml to config.toml.example (for distribution)
- Updated install.sh to handle config setup (copy for users, symlink for --dev)
- Added config.toml to .gitignore
- Created .claude/symlinks/config.toml for easy dev editing
- Script now only looks in ~/.config/hello-zsh/ for config (simplified)

### Enhanced for Public Release
- Added user_name configuration (replaces hardcoded "Wils")
- Added show_weather and show_quote toggles to config
- hello-zsh.py now respects these config options
- Improved install.sh with:
  - Python 3 check
  - User name prompt on first install
  - PATH verification and instructions
  - Better dependency installation guidance
  - Interactive test option after successful install
  - Clear emojis and formatting for better UX

### Added Zinit Plugin Support
- Created hello-zsh.plugin.zsh for ZSH plugin manager compatibility
- Supports Zinit, Oh My Zsh, and other plugin managers
- Auto-runs on shell startup (configurable via HELLO_ZSH_AUTO)
- Includes dependency checking and first-time setup
- Updated README with Zinit installation instructions
- Maintains backward compatibility with install.sh method
- Simplified first-time setup - no interactive prompts, just creates config file
- Removed name prompt from install.sh to match simplified approach
- Reduced bottom padding after quote for more compact display
- Fixed uptime formatting bug (was showing "12, , 34 min" instead of "12h 34m")

### Project Organization
- Created tools/ directory for utility scripts
- Moved generate-font-samples.py and current-fonts-samples.py to tools/
- Created samples/ directory for generated font samples
- Moved font-samples.txt and current-fonts-samples.txt to samples/
- Added screenshot.jpg for GitHub release documentation
- Removed weather API timeout to wait for response when service is slow

## 2025-07-23

### Project Setup
- Created `.claude/` directory structure with planning/, reference/, symlinks/ subdirectories
- Created `changes.md` and `journal.md` tracking files
- Created project-specific `CLAUDE.md` based on template, adapted for Python terminal banner project
- Created `CHANGELOG.md` with initial version 0.1.0
- Created `VERSION` file set to 0.1.0
- Configured project as Python terminal utility with Rich/pyfiglet dependencies

### Greeting Panel Update
- Modified greeting text to use Panel with no borders (border_style="none")
- Applied same padding (1, 4) as system panel for consistency
- Updated both narrow and wide terminal layouts to use greeting_panel
- Tested changes - greeting now appears in borderless panel with proper padding
- Fixed border removal by creating custom NO_BORDER Box style with empty borders
- Added horizontal centering for greeting panel in grid layout using Align wrapper
- Successfully removed all borders from greeting panel while maintaining padding

### Install Script Creation
- Created install.sh script to copy files to ~/.config/hello-zsh
- Script creates config directory, backs up existing files with timestamps
- Copies hello-zsh.py, config.toml, and requirements.txt to config dir
- Creates symlink in ~/.local/bin for easy command access
- Updated to check for Python dependencies instead of auto-installing
- Added rich-gradient to requirements.txt (was missing)
- Script provides instructions for installing missing dependencies

### Development Mode Setup
- Changed from copying files to creating symlinks for active development
- Removed existing copies from ~/.config/hello-zsh
- Created symlinks from config to development directory
- Updated install.sh to create symlinks instead of copying
- Added tracking symlinks in .claude/symlinks directory
- Fixed weather color access bug (using .get() with proper fallbacks)
- Now changes in development directory are immediately reflected

### Simplified Setup
- Removed unnecessary ~/.config/hello-zsh directory entirely
- Updated ~/.local/bin/hello-zsh to symlink directly to development folder
- Simplified install.sh to just create one symlink
- Removed intermediate symlinks from .claude/symlinks
- Now just one direct symlink: ~/.local/bin/hello-zsh → /home/wilst/projects/hello-zsh/hello-zsh.py

### VSCode Terminal Fix
- Fixed issue where banner wasn't displaying in VSCode terminal
- Added detection for TERM_PROGRAM environment variable
- Only clears screen in regular terminals, skips in VSCode for compatibility
- Added hello-zsh to ~/.zshrc for automatic startup on terminal open