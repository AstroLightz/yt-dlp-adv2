#!/bin/bash

PROJECT_URL="https://github.com/AstroLightz/yt-dlp-adv2"
DOWNLOAD_PATH="$HOME/.local/yt-dlp-adv"

# Check if python and pip are installed
if ! command -v python3 >/dev/null 2>&1; then
    echo "Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

echo "(1/2) Downloading script files... "

### Download files

# Use git if available
if command -v git >/dev/null 2>&1; then
    git clone "$PROJECT_URL" "$DOWNLOAD_PATH"

# wget
elif command -v wget >/dev/null 2>&1; then
    wget -O "$DOWNLOAD_PATH" "$PROJECT_URL"

# curl
elif command -v curl >/dev/null 2>&1; then
    curl -o "$DOWNLOAD_PATH" "$PROJECT_URL"

# Error
else
    echo "No download tool found. Please install git, wget, or curl."
    exit 1
fi

### Install

echo "(2/2) Downloading dependencies... "

cd "$DOWNLOAD_PATH" || exit

python -m venv .venv
source "$DOWNLOAD_PATH/.venv/bin/activate"

pip install -r requirements.txt

chmod +x main.py

# Prompt to add alias to bashrc/zshrc
echo "Install complete. This installer can add an alias to your shell's rc file to run yt-dlp-adv. Proceed? (Y/n)"
echo -n ">> "
read -r proceed

if [ "$proceed" != "n" ] && [ "$proceed" != "N" ]; then
    
    if [ -f "$HOME/.bashrc" ] || [ -f "$HOME/.zshrc" ]; then
        if [ -f "$HOME/.bashrc" ]; then
            # Bash
            echo "alias yt-dlp-adv=\"\"$DOWNLOAD_PATH/.venv/bin/python\" \"$DOWNLOAD_PATH/main.py\"\"" >> "$HOME/.bashrc"
            echo "Alias added to your bashrc file. Use \"yt-dlp-adv\" to run yt-dlp-adv."
        fi

        if [ -f "$HOME/.zshrc" ]; then
            # Zsh
            echo "alias yt-dlp-adv=\"\"$DOWNLOAD_PATH/.venv/bin/python\" \"$DOWNLOAD_PATH/main.py\"\"" >> "$HOME/.zshrc"
            echo "Alias added to your zshrc file. Use \"yt-dlp-adv\" to run yt-dlp-adv."
        fi

        echo "Done. Restart your shell or source your rc file to use yt-dlp-adv."
    
    else
        echo "No shell found. Please add an alias to your shell's rc file manually."
    fi

else
    echo "To run yt-dlp-adv, use \"$DOWNLOAD_PATH/.venv/bin/python $DOWNLOAD_PATH/main.py\""

fi