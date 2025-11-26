#!/usr/bin/env python3
"""
GAMEZILLA MEGA COLLECTION VOL. 4 - Main Launcher
Cursed shareware CD experience
"""

import sys
import time
import os
import random
from shareware_gen import SharewareGenerator


class CursedLauncher:
    """The cursed DOS/shareware launcher experience"""

    # ANSI colors
    BLUE_BG = "\033[44m"
    YELLOW_BG = "\033[43m"
    RED_BG = "\033[41m"
    CYAN_BG = "\033[46m"

    TEXT_BLUE = "\033[34m"
    TEXT_YELLOW = "\033[33m"
    TEXT_WHITE = "\033[37m"
    TEXT_RED = "\033[31m"
    TEXT_GREEN = "\033[32m"
    TEXT_CYAN = "\033[36m"
    TEXT_MAGENTA = "\033[35m"

    RESET = "\033[0m"
    BOLD = "\033[1m"
    CLEAR = "\033[2J\033[H"

    def __init__(self):
        self.generator = SharewareGenerator()
        self.programs = self.generator.get_all_programs()
        self.selected_idx = 386  # Program 387
        self.page = 0
        self.items_per_page = 16

    def clear(self):
        """Clear screen"""
        print(self.CLEAR, end="", flush=True)

    def flicker(self):
        """Screen flicker effect"""
        for _ in range(2):
            print("\033[40m" + " " * 2000, end="", flush=True)
            time.sleep(0.08)
            self.clear()
            time.sleep(0.08)

    def print_header(self):
        """Print menu header"""
        header = f"""
{self.BLUE_BG}{self.TEXT_YELLOW}{'═' * 80}{self.RESET}
{self.BLUE_BG}{self.TEXT_YELLOW}  GAMEZILLA MEGA COLLECTION VOL. 4{self.RESET}
{self.BLUE_BG}{self.TEXT_YELLOW}  500 Programs - Your Entertainment Solution!{self.RESET}
{self.BLUE_BG}{self.TEXT_CYAN}  Games • Utilities • Demos • Shareware - All In One Package!{self.RESET}
{self.BLUE_BG}{self.TEXT_YELLOW}{'═' * 80}{self.RESET}
"""
        print(header)

    def print_list(self):
        """Print program list"""
        start = self.page * self.items_per_page
        end = min(start + self.items_per_page, len(self.programs))

        print(f"\n{self.TEXT_YELLOW}[Programs {start+1} - {end} of 500]{self.RESET}\n")

        for i in range(start, end):
            prog = self.programs[i]
            is_selected = (i == self.selected_idx)

            if is_selected:
                line = f"{self.RED_BG}{self.TEXT_YELLOW}► {prog['number']:3d}. {prog['name']:<50}{self.RESET}"
            else:
                marker = "✦" if prog["is_real"] else " "
                line = f"  {self.TEXT_GREEN}{prog['number']:3d}. {prog['name']:<48}{self.TEXT_CYAN}{marker}{self.RESET}"

            print(line)

    def print_footer(self):
        """Print menu footer"""
        footer = f"""
{self.BLUE_BG}{self.TEXT_YELLOW}{'═' * 80}{self.RESET}
{self.CYAN_BG}{self.TEXT_WHITE} ↑/↓: Navigate  ENTER: Launch  P/N: Page  Q: Quit{self.RESET}
{self.BLUE_BG}{self.TEXT_YELLOW}{'═' * 80}{self.RESET}
"""
        print(footer)

    def init_screen(self):
        """Show initialization screen"""
        self.clear()

        init = f"""
{self.BLUE_BG}{self.TEXT_YELLOW}
{'═' * 80}
  INITIALIZING GAMEZILLA MEGA COLLECTION...
{'═' * 80}
{self.RESET}

{self.TEXT_GREEN}
  Checking system memory.................... OK
  Loading DOS drivers....................... OK
  Initializing video adapter............... OK
  Detecting graphics card.................. OK
  Loading extended memory.................. OK
  Checking CD-ROM drive.................... OK
  Mounting CD filesystems.................. OK
  Loading system fonts..................... OK
  Initializing mouse driver................ OK
  Loading configuration files.............. OK
  Decompressing program catalog............ OK
  Verifying checksums...................... OK
  Calibrating system timer................. OK
{self.RESET}

{self.TEXT_CYAN}
  Press ENTER to continue...
{self.RESET}
"""
        print(init)
        input()

    def show_loading(self, prog_name):
        """Show fake loading screen"""
        self.clear()

        loading = f"""
{self.RED_BG}{self.TEXT_YELLOW}
{'═' * 80}
  LOADING PROGRAM...
{'═' * 80}
{self.RESET}

{self.TEXT_YELLOW}
  Program: {prog_name}

{self.TEXT_GREEN}
  Loading executable...................
  Decompressing data files..............
  Checking system resources.............
  Initializing graphics engine..........
  Loading assets........................
  Verifying file integrity..............
  Preparing memory......................

{self.TEXT_CYAN}
  [{'█' * 40}] 100%

{self.TEXT_WHITE}
  Starting in 3 seconds...
{self.RESET}
"""
        print(loading)
        sys.stdout.flush()
        time.sleep(3)

    def show_error(self, prog):
        """Show error for fake program"""
        self.clear()

        error = f"""
{self.RED_BG}{self.TEXT_YELLOW}
{'═' * 80}
  PROGRAM NOT FOUND - ERROR
{'═' * 80}
{self.RESET}

{self.TEXT_RED}
  File: {prog['executable']}

  This program is listed in the catalog but is not installed.

  Installation Disk 1 of 3 required.

  Please check the CD integrity or reinstall from original floppies.
{self.RESET}

{self.TEXT_YELLOW}
  Press ENTER to return to menu...
{self.RESET}
"""
        print(error)
        input()

    def launch_program(self, prog_num):
        """Launch program"""
        prog = self.generator.get_program(prog_num)
        if not prog:
            return

        if not prog["is_real"]:
            self.show_error(prog)
            return

        # Real program - launch correct version
        self.show_loading(prog["name"])

        try:
            executable = prog.get("executable", "v1")

            if executable == "v1":
                # Launch V1 (original game)
                if os.path.exists("src/game_loop.py"):
                    # We're in v1-doofenstein directory
                    sys.path.insert(0, "src")
                    from game_loop import main
                    main()
                elif os.path.exists("../v1-doofenstein/src/game_loop.py"):
                    os.system("cd ../v1-doofenstein && python3 src/main.py")
                else:
                    print(f"\n{self.TEXT_RED}[ERROR] V1 not found!{self.RESET}")
                    input("Press ENTER...")

            elif executable == "v2":
                # Launch V2 (immersive sim)
                if os.path.exists("../v2-immersive-sim/src/main.py"):
                    self.clear()
                    os.system("cd ../v2-immersive-sim && python3 src/main.py")
                elif os.path.exists("v2-immersive-sim/src/main.py"):
                    self.clear()
                    os.system("cd v2-immersive-sim && python3 src/main.py")
                else:
                    print(f"\n{self.TEXT_RED}[ERROR] V2 not found!{self.RESET}")
                    print("Make sure v2-immersive-sim/src/main.py exists.")
                    input("Press ENTER...")

            elif executable == "v3":
                # Launch V3 (Eastland Mall - Graphical with AI)
                if os.path.exists("../v3-eastland/src/main_pygame.py"):
                    self.clear()
                    os.system("cd ../v3-eastland && python3 src/main_pygame.py")
                elif os.path.exists("v3-eastland/src/main_pygame.py"):
                    self.clear()
                    os.system("cd v3-eastland && python3 src/main_pygame.py")
                else:
                    print(f"\n{self.TEXT_RED}[ERROR] V3 not found!{self.RESET}")
                    print("Make sure v3-eastland/src/main_pygame.py exists.")
                    print("Requires pygame: pip install pygame")
                    input("Press ENTER...")

            elif executable == "v4":
                # Launch V4 (Renderist Mall OS - Cloud-driven world)
                if os.path.exists("../v4-renderist/src/main.py"):
                    self.clear()
                    os.system("cd ../v4-renderist && python3 src/main.py")
                elif os.path.exists("v4-renderist/src/main.py"):
                    self.clear()
                    os.system("cd v4-renderist && python3 src/main.py")
                else:
                    print(f"\n{self.TEXT_RED}[ERROR] V4 not found!{self.RESET}")
                    print("Make sure v4-renderist/src/main.py exists.")
                    input("Press ENTER...")

            elif executable == "v5":
                # V5 is documentation, show info
                self.clear()
                print("\n" + "=" * 70)
                print("EASTLAND MALL V5 - CRD RECONSTRUCTION")
                print("=" * 70)
                print("\nV5 is a documentation/reconstruction project.")
                print("Check the v5-eastland/ directory for:")
                print("  - PHOTO_CLASSIFICATION_TABLE_V1_COMPLETE.md")
                print("  - MALL_MAP_V5_PROPOSAL.json")
                print("  - README_ARCHITECTURAL_CONTEXT.md")
                print("\nPress ENTER to continue...")
                input()

            elif executable == "v6":
                # Launch V6 (Next Generation - placeholder)
                if os.path.exists("../v6-nextgen/src/main.py"):
                    self.clear()
                    os.system("cd ../v6-nextgen && python3 src/main.py")
                elif os.path.exists("v6-nextgen/src/main.py"):
                    self.clear()
                    os.system("cd v6-nextgen && python3 src/main.py")
                else:
                    print(f"\n{self.TEXT_RED}[ERROR] V6 not found!{self.RESET}")
                    print("Make sure v6-nextgen/src/main.py exists.")
                    input("Press ENTER...")

            else:
                # Fallback to old behavior
                if os.path.exists("glitchdex-mall.exe"):
                    os.system("glitchdex-mall.exe")
                elif os.path.exists("dist/glitchdex-mall/glitchdex-mall.exe"):
                    os.system("dist/glitchdex-mall/glitchdex-mall.exe")
                else:
                    print(f"\n{self.TEXT_RED}[ERROR] Game not found!{self.RESET}")
                    input("Press ENTER...")

        except Exception as e:
            self.clear()
            print(f"{self.TEXT_RED}Error: {e}{self.RESET}")
            import traceback
            traceback.print_exc()
            input()

    def run(self):
        """Main launcher loop"""
        self.init_screen()
        self.flicker()

        while True:
            self.clear()
            self.print_header()
            self.print_list()
            self.print_footer()

            try:
                cmd = input(f"\n{self.TEXT_CYAN}> {self.RESET}").strip().lower()

                if cmd == "q":
                    self.clear()
                    print(f"{self.TEXT_YELLOW}Thank you for using GAMEZILLA MEGA COLLECTION!{self.RESET}\n")
                    break

                elif cmd == "up" or cmd == "w":
                    if self.selected_idx > 0:
                        self.selected_idx -= 1

                elif cmd == "down" or cmd == "s":
                    if self.selected_idx < len(self.programs) - 1:
                        self.selected_idx += 1

                elif cmd == "n":
                    next_page = (self.page + 1) * self.items_per_page
                    if next_page < len(self.programs):
                        self.page += 1
                        self.selected_idx = next_page

                elif cmd == "p":
                    if self.page > 0:
                        self.page -= 1
                        self.selected_idx = self.page * self.items_per_page

                elif cmd == "" or cmd == "enter":
                    prog = self.programs[self.selected_idx]
                    self.launch_program(prog["number"])

                # Allow typing program number
                elif cmd.isdigit():
                    prog_num = int(cmd)
                    if 1 <= prog_num <= 500:
                        self.launch_program(prog_num)

            except (EOFError, KeyboardInterrupt):
                self.clear()
                print(f"{self.TEXT_YELLOW}Exiting...{self.RESET}\n")
                break
            except Exception as e:
                pass


def main():
    """Entry point"""
    try:
        launcher = CursedLauncher()
        launcher.run()
    except KeyboardInterrupt:
        print("\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
