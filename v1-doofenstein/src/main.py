#!/usr/bin/env python3
"""
GLITCHDEX MALL ENGINE – Entry Point
A first-person dungeon crawler set in a xennial shopping mall.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))

from game_loop import main

if __name__ == "__main__":
    main()
