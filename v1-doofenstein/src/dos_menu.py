"""
DOS Menu System - Cursed Shareware Launcher
Fire cursor, colored text, ASCII art borders, authentic 1990s horror
"""

import sys
import time
import os
import random
import subprocess
from shareware_gen import SharewareGenerator


class FireCursor:
    """Animated fire cursor that follows the mouse (sort of)"""

    def __init__(self):
        self.fire_frames = [
            "🔥",
            "💥",
            "✦",
            "∞",
            "⚡",
        ]
        self.frame = 0
        self.lag_buffer = []
        self.max_lag = 3

    def get_next_frame(self):
        """Get next frame of fire cursor"""
        self.frame = (self.frame + 1) % len(self.fire_frames)
        return self.fire_frames[self.frame]


class DOSMenu:
    """Authentic 1990s DOS/Windows menu system"""

    # ANSI color codes
    BLUE = "\033[44m"
    YELLOW = "\033[43m"
    WHITE = "\033[47m"
    RED = "\033[41m"
    GREEN = "\033[42m"
    CYAN = "\033[46m"

    TEXT_BLUE = "\033[34m"
    TEXT_YELLOW = "\033[33m"
    TEXT_WHITE = "\033[37m"
    TEXT_RED = "\033[31m"
    TEXT_GREEN = "\033[32m"
    TEXT_CYAN = "\033[36m"

    RESET = "\033[0m"
    BOLD = "\033[1m"
    CLEAR = "\033[2J\033[H"

    def __init__(self):
        self.generator = SharewareGenerator()
        self.cursor = FireCursor()
        self.selected_index = 386  # Start at program 387 (0-indexed)
        self.programs = self.generator.get_all_programs()
        self.page = 0
        self.programs_per_page = 15

    def clear_screen(self):
        """Clear screen with DOS-style jank"""
        # Quick flickering effect
        print(self.CLEAR, end="")
        sys.stdout.flush()

    def screen_flicker(self):
        """Dramatic screen flicker at startup"""
        for _ in range(3):
            print("\033[40m" + " " * 80 * 24)  # Black screen
            sys.stdout.flush()
            time.sleep(0.05)
            self.clear_screen()
            time.sleep(0.05)

    def draw_header(self):
        """Draw menu header"""
        header = f"""
{self.BLUE}{self.TEXT_YELLOW}╔════════════════════════════════════════════════════════════════════════════╗{self.RESET}
{self.BLUE}{self.TEXT_YELLOW}║                    GAMEZILLA MEGA COLLECTION VOL. 4                          ║{self.RESET}
{self.BLUE}{self.TEXT_YELLOW}║                                                                            ║{self.RESET}
{self.BLUE}{self.TEXT_CYAN}║  Your Complete Solution for Entertainment & Productivity - 1998 Edition     ║{self.RESET}
{self.BLUE}{self.TEXT_YELLOW}║                          500 Programs Ready to Use!                          ║{self.RESET}
{self.BLUE}{self.TEXT_YELLOW}╚════════════════════════════════════════════════════════════════════════════╝{self.RESET}
"""
        print(header)

    def draw_program_list(self):
        """Draw scrollable program list"""
        start_idx = self.page * self.programs_per_page
        end_idx = min(start_idx + self.programs_per_page, len(self.programs))

        print(f"\n{self.BLUE}{self.TEXT_YELLOW}Program Selection (Page {self.page + 1}){self.RESET}\n")

        for i, idx in enumerate(range(start_idx, end_idx)):
            prog = self.programs[idx]
            is_selected = idx == self.selected_index

            # Highlight selected program
            if is_selected:
                line = f"{self.WHITE}{self.TEXT_RED}▶ {prog['number']:3d}. {prog['name']:<50}{self.RESET}"
            else:
                marker = " ✦" if prog["is_real"] else "  "
                line = f"  {prog['number']:3d}. {prog['name']:<48}{marker}{self.RESET}"

            print(line)

    def draw_footer(self):
        """Draw menu footer"""
        footer = f"""
{self.BLUE}{self.TEXT_YELLOW}╔════════════════════════════════════════════════════════════════════════════╗{self.RESET}
{self.BLUE}{self.TEXT_CYAN}║  UP/DOWN: Navigate  |  ENTER: Launch  |  PgUp/PgDn: Scroll  |  Q: Quit       ║{self.RESET}
{self.BLUE}{self.TEXT_YELLOW}╚════════════════════════════════════════════════════════════════════════════╝{self.RESET}
"""
        print(footer)

    def draw_initialization_screen(self):
        """Draw fake initialization/loading screen"""
        self.clear_screen()

        init_text = f"""
{self.BLUE}{self.TEXT_YELLOW}
╔════════════════════════════════════════════════════════════════════════════╗
║                       INITIALIZING SYSTEM...                              ║
╚════════════════════════════════════════════════════════════════════════════╝

{self.TEXT_GREEN}
Checking system memory..................OK
Loading DOS drivers......................OK
Initializing video adapter...............OK
Detecting graphics card..................OK
Loading extended memory..................OK
Checking CD-ROM drive....................OK
Mounting CD filesystems..................OK
Loading system fonts.....................OK
Initializing mouse driver.................OK
Loading configuration files..............OK
Decompressing program catalog............OK
Verifying checksums......................OK

{self.TEXT_CYAN}
════════════════════════════════════════════════════════════════════════════

  Press any key to continue to GAMEZILLA MEGA COLLECTION...

{self.RESET}
"""
        print(init_text)
        sys.stdout.flush()
        time.sleep(2)

    def show_loading_screen(self, program_name):
        """Show loading screen before launching program"""
        self.clear_screen()

        loading = f"""
{self.RED}{self.BOLD}
╔════════════════════════════════════════════════════════════════════════════╗
║                      LOADING PROGRAM...                                   ║
╚════════════════════════════════════════════════════════════════════════════╝

{self.TEXT_YELLOW}
Program: {program_name}

{self.TEXT_GREEN}
Loading executable.......................
Decompressing data files..................
Checking system resources.................
Initializing graphics engine..............
Loading assets...........................
Verifying file integrity..................
Preparing memory..........................

{self.TEXT_CYAN}
[████████████████████████████████████████] 100%

{self.TEXT_WHITE}
Starting application in 3 seconds...

{self.RESET}
"""
        print(loading)
        sys.stdout.flush()
        time.sleep(3)

    def launch_program(self, program_number):
        """Launch the selected program"""
        prog = self.generator.get_program(program_number)
        if not prog:
            return False

        if not prog["is_real"]:
            # Fake program - show error message
            self.clear_screen()
            print(f"""
{self.RED}
╔════════════════════════════════════════════════════════════════════════════╗
║                         PROGRAM NOT FOUND                                 ║
╚════════════════════════════════════════════════════════════════════════════╝

{self.TEXT_RED}
Error: {prog['executable']} not found.

This program is listed in the catalog but is not installed on this CD.
Please check the CD integrity or reinstall from the original floppy disks.

{self.TEXT_YELLOW}
Installation Disk 1 of 3 required.

Press any key to return to menu...
{self.RESET}
""")
            sys.stdout.flush()
            input()
            return False

        # Real program - launch it
        self.show_loading_screen(prog["name"])

        # Try to launch glitchdex-mall.exe
        try:
            # Look for executable in the same directory or dist/
            exe_paths = [
                "glitchdex-mall.exe",
                "dist/glitchdex-mall/glitchdex-mall.exe",
                "../dist/glitchdex-mall/glitchdex-mall.exe",
            ]

            for exe_path in exe_paths:
                if os.path.exists(exe_path):
                    subprocess.run(exe_path, check=False)
                    return True

            # If .exe not found, try running with Python
            import sys
            sys.path.insert(0, "src")
            from game_loop import main
            main()
            return True

        except Exception as e:
            self.clear_screen()
            print(f"""
{self.RED}
╔════════════════════════════════════════════════════════════════════════════╗
║                       EXECUTION ERROR                                     ║
╚════════════════════════════════════════════════════════════════════════════╝

{self.TEXT_RED}
Error launching {prog['executable']}:
{str(e)}

{self.TEXT_YELLOW}
This program may require additional system resources or dependencies.
Try running from DOS 6.2 or Windows 95.

Press any key to return to menu...
{self.RESET}
""")
            sys.stdout.flush()
            input()
            return False

    def handle_input(self):
        """Handle user input"""
        # Try to get input without blocking
        try:
            if sys.stdin.isatty():
                import tty
                import termios
                ch = sys.stdin.read(1).lower()
            else:
                ch = input().lower()[0] if input() else ""
        except:
            return

        if ch == "q":
            return False  # Quit

        elif ch == "\x1b":  # Arrow keys
            try:
                ch = sys.stdin.read(2)
                if ch == "[A":  # Up
                    if self.selected_index > 0:
                        self.selected_index -= 1
                elif ch == "[B":  # Down
                    if self.selected_index < len(self.programs) - 1:
                        self.selected_index += 1
            except:
                pass

        elif ch == "\n" or ch == " ":  # Enter or Space
            self.launch_program(self.programs[self.selected_index]["number"])

        return True

    def run(self):
        """Main menu loop"""
        # Show initialization
        self.draw_initialization_screen()
        self.screen_flicker()

        running = True
        while running:
            self.clear_screen()
            self.draw_header()
            self.draw_program_list()
            self.draw_footer()

            # Show cursor animation
            cursor_frame = self.cursor.get_next_frame()
            print(f"\n{self.TEXT_CYAN}{cursor_frame}{self.RESET}", end="", flush=True)

            time.sleep(0.1)
            # In a real implementation, we'd handle async input here

            # For now, just keep showing the menu
            # User can navigate with arrow keys and press Enter
            running = self.handle_input()

        self.clear_screen()
        print(f"{self.TEXT_YELLOW}Thank you for using GAMEZILLA MEGA COLLECTION!{self.RESET}\n")


if __name__ == "__main__":
    menu = DOSMenu()
    menu.run()
