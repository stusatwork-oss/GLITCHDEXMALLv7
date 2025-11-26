#!/bin/bash
# GLITCHDEX MALL - Mac/Linux Launcher
# Just run the game. No configuration. No complexity.

echo ""
echo "═══════════════════════════════════════════════════════════════════════"
echo "GLITCHDEX MALL ENGINE"
echo "═══════════════════════════════════════════════════════════════════════"
echo ""

# Check if Python exists
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not found!"
    echo ""
    echo "Please install Python 3.8+ from https://www.python.org"
    echo "Or use your package manager:"
    echo "  macOS: brew install python3"
    echo "  Ubuntu/Debian: sudo apt install python3"
    echo "  Fedora: sudo dnf install python3"
    echo ""
    read -p "Press ENTER to exit..."
    exit 1
fi

# Run the launcher (cursed shareware CD menu)
echo "Starting GAMEZILLA MEGA COLLECTION launcher..."
echo ""

python3 src/launcher.py

read -p "Press ENTER to exit..."
