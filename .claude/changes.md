# Changes Log

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