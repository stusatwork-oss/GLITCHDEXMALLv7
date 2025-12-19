#!/usr/bin/env python3
"""
NINJA SABOTEUR: MAIN LAUNCHER (V8)
Wrapper to launch the visual runtime.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

try:
    from visual_runtime import VisualRuntime
except ImportError as e:
    print(f"CRITICAL ERROR: Failed to import VisualRuntime: {e}")
    print("Ensure all dependencies are installed: pip install -r requirements.txt")
    sys.exit(1)

def main():
    print("==========================================")
    print(" NINJA SABOTEUR - V8 LAB BUILD")
    print("==========================================")

    try:
        app = VisualRuntime()
        app.run()
    except Exception as e:
        print(f"RUNTIME ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
