#!/bin/bash

# Setup convenient alias for launching the application
# Run this once: bash setup_alias.sh
# Then you can use: audio-enhance (from anywhere)

ALIAS_CMD='alias audio-enhance="cd /Users/joebradley/Projects/ihor-audio-main/reaper-audio-enhancement && bash launch.sh"'

# Add to ~/.zshrc (for zsh shell)
if [ -f ~/.zshrc ]; then
    if ! grep -q "audio-enhance" ~/.zshrc; then
        echo "" >> ~/.zshrc
        echo "# REAPER Audio Enhancement alias" >> ~/.zshrc
        echo "$ALIAS_CMD" >> ~/.zshrc
        echo "✓ Alias added to ~/.zshrc"
    else
        echo "✓ Alias already exists in ~/.zshrc"
    fi
fi

# Add to ~/.bash_profile (for bash shell)
if [ -f ~/.bash_profile ]; then
    if ! grep -q "audio-enhance" ~/.bash_profile; then
        echo "" >> ~/.bash_profile
        echo "# REAPER Audio Enhancement alias" >> ~/.bash_profile
        echo "$ALIAS_CMD" >> ~/.bash_profile
        echo "✓ Alias added to ~/.bash_profile"
    else
        echo "✓ Alias already exists in ~/.bash_profile"
    fi
fi

echo ""
echo "Setup complete! You can now use:"
echo "  audio-enhance"
echo ""
echo "From any directory to launch the application."
echo ""
echo "Restart your terminal or run: source ~/.zshrc"
