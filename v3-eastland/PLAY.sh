#!/bin/bash
#
# EASTLAND MALL - V3
# A dying mall from the late 80s.
# Something is wrong here.
#

clear

echo ""
echo "  ╔════════════════════════════════════════════════════════════╗"
echo "  ║                                                            ║"
echo "  ║   E A S T L A N D   M A L L                                ║"
echo "  ║                                                            ║"
echo "  ║   GLITCHDEX V3                                             ║"
echo "  ║                                                            ║"
echo "  ╚════════════════════════════════════════════════════════════╝"
echo ""
echo "  Select mode:"
echo ""
echo "  [1] Graphical (Pygame) - Full raycaster with era-bleed"
echo "  [2] Text Mode - Terminal-based adventure"
echo ""
read -p "  > " mode

# Navigate to script directory
cd "$(dirname "$0")"

# Check Python
PYTHON=""
if command -v python3 &> /dev/null; then
    PYTHON="python3"
elif command -v python &> /dev/null; then
    PYTHON="python"
else
    echo "  ERROR: Python not found."
    echo "  Please install Python 3 to play."
    exit 1
fi

case $mode in
    1)
        echo ""
        echo "  Starting graphical mode..."
        echo "  (Requires pygame: pip install pygame)"
        echo ""
        $PYTHON src/main_pygame.py
        ;;
    2)
        echo ""
        echo "  Starting text mode..."
        echo ""
        $PYTHON src/main.py
        ;;
    *)
        echo ""
        echo "  Defaulting to graphical mode..."
        echo ""
        $PYTHON src/main_pygame.py
        ;;
esac
