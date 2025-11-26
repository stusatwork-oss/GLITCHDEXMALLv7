#!/usr/bin/env python3
"""
GAMEZILLA MEGA COLLECTION VOL. 4 - GUI Launcher
Mid-90s style mouse-clickable 16-color interface
Windows 95-inspired shareware CD experience
"""

import curses
import sys
import os
import time
import subprocess
from shareware_gen_v2 import SharewareGeneratorV2


class GUI_Launcher:
    """Mid-90s style GUI launcher with mouse support"""

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.generator = SharewareGeneratorV2()
        self.programs = self.generator.get_all_programs()
        self.selected_idx = 386  # Program 387 (GLITCHDEX MALL V1)
        self.page = 0
        self.items_per_page = 10
        self.running = True

        # Initialize colors
        self.init_colors()

        # Enable mouse
        curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)

        # Hide cursor
        curses.curs_set(0)

    def init_colors(self):
        """Initialize 16-color VGA palette"""
        curses.start_color()
        curses.use_default_colors()

        # Classic VGA 16-color pairs (matching Windows 95 era)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)      # Title bar
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)      # Window bg
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLUE)     # Highlighted text
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_RED)       # Selected item
        curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_WHITE)     # Button
        curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)     # Button pressed
        curses.init_pair(7, curses.COLOR_GREEN, curses.COLOR_BLUE)      # Real programs
        curses.init_pair(8, curses.COLOR_CYAN, curses.COLOR_BLUE)       # Info text
        curses.init_pair(9, curses.COLOR_BLACK, curses.COLOR_GREEN)     # Status bar
        curses.init_pair(10, curses.COLOR_YELLOW, curses.COLOR_BLACK)   # Warning
        curses.init_pair(11, curses.COLOR_RED, curses.COLOR_WHITE)      # Error
        curses.init_pair(12, curses.COLOR_MAGENTA, curses.COLOR_BLUE)   # Special marker

    def draw_window(self, y, x, height, width, title=""):
        """Draw a 3D-style window with shadow"""
        # Shadow
        for dy in range(1, height + 1):
            self.stdscr.addstr(y + dy, x + 2, "  " * (width // 2), curses.color_pair(6))

        # Main window
        self.stdscr.attron(curses.color_pair(2))
        for dy in range(height):
            self.stdscr.addstr(y + dy, x, " " * width)
        self.stdscr.attroff(curses.color_pair(2))

        # Border
        self.stdscr.attron(curses.color_pair(2))
        # Top border
        self.stdscr.addstr(y, x, "┌" + "─" * (width - 2) + "┐")
        # Side borders
        for dy in range(1, height - 1):
            self.stdscr.addstr(y + dy, x, "│")
            self.stdscr.addstr(y + dy, x + width - 1, "│")
        # Bottom border
        self.stdscr.addstr(y + height - 1, x, "└" + "─" * (width - 2) + "┘")
        self.stdscr.attroff(curses.color_pair(2))

        # Title bar
        if title:
            self.stdscr.attron(curses.color_pair(1))
            title_text = f" {title} "
            self.stdscr.addstr(y, x + 2, title_text)
            self.stdscr.attroff(curses.color_pair(1))

    def draw_button(self, y, x, width, label, is_pressed=False):
        """Draw a 3D button"""
        pair = curses.color_pair(6 if is_pressed else 5)

        self.stdscr.attron(pair)
        # Button with padding
        btn_text = label.center(width - 2)
        self.stdscr.addstr(y, x, f"[{btn_text}]")
        self.stdscr.attroff(pair)

        return (y, x, y, x + width)  # Return clickable area

    def draw_header(self):
        """Draw main window header"""
        height, width = self.stdscr.getmaxyx()

        # Main window
        self.draw_window(0, 0, height - 1, width - 1, "GAMEZILLA MEGA COLLECTION VOL. 4")

        # Subtitle
        self.stdscr.attron(curses.color_pair(3) | curses.A_BOLD)
        subtitle = "500 Programs - Your Entertainment Solution!"
        self.stdscr.addstr(2, (width - len(subtitle)) // 2, subtitle)
        self.stdscr.attroff(curses.color_pair(3) | curses.A_BOLD)

        # Info line
        self.stdscr.attron(curses.color_pair(8))
        info = "Games • Utilities • Demos • Shareware - All In One Package!"
        self.stdscr.addstr(3, (width - len(info)) // 2, info)
        self.stdscr.attroff(curses.color_pair(8))

    def draw_program_list(self):
        """Draw the program list with mouse-clickable items"""
        height, width = self.stdscr.getmaxyx()
        start_y = 5
        start_x = 3

        start = self.page * self.items_per_page
        end = min(start + self.items_per_page, len(self.programs))

        # Page indicator
        self.stdscr.attron(curses.color_pair(3))
        page_info = f"Programs {start+1}-{end} of 500 (Page {self.page+1})"
        self.stdscr.addstr(start_y, start_x, page_info)
        self.stdscr.attroff(curses.color_pair(3))

        # Draw list
        for i, prog_idx in enumerate(range(start, end)):
            prog = self.programs[prog_idx]
            y = start_y + 2 + i
            is_selected = (prog_idx == self.selected_idx)

            # Selection highlight
            if is_selected:
                self.stdscr.attron(curses.color_pair(4) | curses.A_BOLD)
                marker = "►"
            else:
                if prog["is_real"]:
                    self.stdscr.attron(curses.color_pair(7))
                    marker = "●"
                else:
                    self.stdscr.attron(curses.color_pair(2))
                    marker = " "

            # Draw item
            item_text = f"{marker} {prog['number']:3d}. {prog['name']:<45}"
            self.stdscr.addstr(y, start_x, item_text[:width - 6])

            if is_selected:
                self.stdscr.attroff(curses.color_pair(4) | curses.A_BOLD)
            else:
                if prog["is_real"]:
                    self.stdscr.attroff(curses.color_pair(7))
                else:
                    self.stdscr.attroff(curses.color_pair(2))

    def draw_buttons(self):
        """Draw control buttons"""
        height, width = self.stdscr.getmaxyx()
        button_y = height - 4

        # Button positions
        self.button_areas = {}

        # Launch button
        x = 5
        area = self.draw_button(button_y, x, 12, "LAUNCH")
        self.button_areas["launch"] = area

        # Prev Page button
        x += 14
        area = self.draw_button(button_y, x, 12, "< PREV")
        self.button_areas["prev"] = area

        # Next Page button
        x += 14
        area = self.draw_button(button_y, x, 12, "NEXT >")
        self.button_areas["next"] = area

        # Quit button
        x += 14
        area = self.draw_button(button_y, x, 12, "QUIT")
        self.button_areas["quit"] = area

    def draw_status_bar(self):
        """Draw status bar"""
        height, width = self.stdscr.getmaxyx()

        self.stdscr.attron(curses.color_pair(9))
        status = " Mouse: Click to select • Keyboard: ↑↓ Navigate, ENTER Launch, Q Quit "
        self.stdscr.addstr(height - 2, 0, status.ljust(width - 1))
        self.stdscr.attroff(curses.color_pair(9))

    def draw_program_info(self):
        """Draw info about selected program"""
        height, width = self.stdscr.getmaxyx()
        info_y = height - 9
        info_x = 3

        prog = self.programs[self.selected_idx]

        self.stdscr.attron(curses.color_pair(8))
        self.stdscr.addstr(info_y, info_x, "─" * (width - 6))

        self.stdscr.addstr(info_y + 1, info_x, f"Selected: {prog['name']}")
        self.stdscr.addstr(info_y + 2, info_x, f"Type: {prog['genre'].upper()}")

        if prog["is_real"]:
            self.stdscr.attron(curses.color_pair(7) | curses.A_BOLD)
            self.stdscr.addstr(info_y + 3, info_x, "Status: ● INSTALLED - Ready to launch!")
            self.stdscr.attroff(curses.color_pair(7) | curses.A_BOLD)
        else:
            self.stdscr.attron(curses.color_pair(10))
            self.stdscr.addstr(info_y + 3, info_x, "Status: Not installed (requires Disk 1 of 3)")
            self.stdscr.attroff(curses.color_pair(10))

        self.stdscr.addstr(info_y + 4, info_x, "─" * (width - 6))
        self.stdscr.attroff(curses.color_pair(8))

    def is_in_area(self, y, x, area):
        """Check if coordinates are in clickable area"""
        y1, x1, y2, x2 = area
        return y1 <= y <= y2 and x1 <= x <= x2

    def handle_mouse(self, mouse_y, mouse_x):
        """Handle mouse clicks"""
        # Check if clicked on program list
        start_y = 7
        start = self.page * self.items_per_page
        end = min(start + self.items_per_page, len(self.programs))

        for i in range(end - start):
            if mouse_y == start_y + i:
                self.selected_idx = start + i
                return

        # Check button clicks
        for btn_name, area in self.button_areas.items():
            if self.is_in_area(mouse_y, mouse_x, area):
                if btn_name == "launch":
                    self.launch_program()
                elif btn_name == "prev":
                    self.prev_page()
                elif btn_name == "next":
                    self.next_page()
                elif btn_name == "quit":
                    self.running = False

    def prev_page(self):
        """Go to previous page"""
        if self.page > 0:
            self.page -= 1
            self.selected_idx = self.page * self.items_per_page

    def next_page(self):
        """Go to next page"""
        next_page = (self.page + 1) * self.items_per_page
        if next_page < len(self.programs):
            self.page += 1
            self.selected_idx = next_page

    def show_loading(self, prog_name):
        """Show loading screen"""
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()

        self.draw_window(5, 10, 10, width - 20, "LOADING")

        self.stdscr.attron(curses.color_pair(3))
        self.stdscr.addstr(7, 15, f"Program: {prog_name}")
        self.stdscr.attroff(curses.color_pair(3))

        self.stdscr.attron(curses.color_pair(7))
        loading_steps = [
            "Loading executable...",
            "Decompressing data files...",
            "Checking system resources...",
            "Initializing graphics engine...",
            "Loading assets...",
        ]
        for i, step in enumerate(loading_steps):
            self.stdscr.addstr(9 + i, 15, f"✓ {step}")

        self.stdscr.attroff(curses.color_pair(7))

        self.stdscr.refresh()
        time.sleep(2)

    def show_error(self, prog):
        """Show error for uninstalled program"""
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()

        self.draw_window(5, 10, 12, width - 20, "ERROR - Program Not Found")

        self.stdscr.attron(curses.color_pair(11) | curses.A_BOLD)
        self.stdscr.addstr(7, 15, "FILE NOT FOUND")
        self.stdscr.attroff(curses.color_pair(11) | curses.A_BOLD)

        self.stdscr.attron(curses.color_pair(2))
        self.stdscr.addstr(9, 15, f"File: {prog['executable']}")
        self.stdscr.addstr(11, 15, "This program is listed in the catalog but")
        self.stdscr.addstr(12, 15, "is not installed.")
        self.stdscr.addstr(14, 15, "Installation Disk 1 of 3 required.")
        self.stdscr.attroff(curses.color_pair(2))

        self.stdscr.attron(curses.color_pair(9))
        self.stdscr.addstr(16, 15, "Press any key to return...")
        self.stdscr.attroff(curses.color_pair(9))

        self.stdscr.refresh()
        self.stdscr.getch()

    def launch_program(self):
        """Launch selected program"""
        prog = self.programs[self.selected_idx]

        if not prog["is_real"]:
            self.show_error(prog)
            return

        self.show_loading(prog["name"])

        # Reset terminal
        curses.endwin()

        try:
            executable = prog.get("executable", "")

            if executable == "v1":
                self._launch_version("v1-doofenstein", "src/main.py")
            elif executable == "v2":
                self._launch_version("v2-immersive-sim", "src/main.py")
            elif executable == "v3":
                self._launch_version("v3-eastland", "src/main_pygame.py")
            elif executable == "v4":
                self._launch_version("v4-renderist", "src/main.py")
            elif executable == "v5":
                self._launch_version("v5-eastland", "src/main.py", is_docs=True)
            elif executable == "v6":
                self._launch_version("v6-nextgen", "src/main.py")
            else:
                print(f"\n[ERROR] Unknown version: {executable}")
                input("Press ENTER...")

        except Exception as e:
            print(f"\n[ERROR] {e}")
            import traceback
            traceback.print_exc()
            input("Press ENTER...")

        # Restart curses
        self.stdscr = curses.initscr()
        self.init_colors()
        curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
        curses.curs_set(0)

    def _launch_version(self, version_dir, main_file, is_docs=False):
        """Helper to launch a specific version"""
        paths_to_try = [
            os.path.join("archive", version_dir, main_file),
            os.path.join("..", "archive", version_dir, main_file),
            os.path.join(version_dir, main_file),  # Fallback
        ]

        for path in paths_to_try:
            if os.path.exists(path):
                if is_docs:
                    # V5 is documentation, just show info
                    print("\n" + "=" * 70)
                    print("EASTLAND MALL V5 - CRD RECONSTRUCTION (ARCHIVED)")
                    print("=" * 70)
                    print("\nV5 is a documentation/reconstruction project.")
                    print("V5 has been archived. Check archive/v5-eastland/ for:")
                    print("  - PHOTO_CLASSIFICATION_TABLE_V1_COMPLETE.md")
                    print("  - MALL_MAP_V5_PROPOSAL.json")
                    print("  - README_ARCHITECTURAL_CONTEXT.md")
                    print("\nV5 measurements are now canonical foundation for V6.")
                    print("\nPress ENTER to continue...")
                    input()
                else:
                    os.system(f"cd {os.path.dirname(path)} && python3 {os.path.basename(path)}")
                return

        print(f"\n[ERROR] {version_dir} not found!")
        print(f"Make sure {version_dir}/{main_file} exists.")
        input("Press ENTER...")

    def run(self):
        """Main loop"""
        while self.running:
            self.stdscr.clear()
            self.draw_header()
            self.draw_program_list()
            self.draw_program_info()
            self.draw_buttons()
            self.draw_status_bar()
            self.stdscr.refresh()

            try:
                key = self.stdscr.getch()

                if key == ord('q') or key == ord('Q'):
                    self.running = False
                elif key == curses.KEY_UP:
                    if self.selected_idx > 0:
                        self.selected_idx -= 1
                        # Update page if needed
                        if self.selected_idx < self.page * self.items_per_page:
                            self.page = self.selected_idx // self.items_per_page
                elif key == curses.KEY_DOWN:
                    if self.selected_idx < len(self.programs) - 1:
                        self.selected_idx += 1
                        # Update page if needed
                        if self.selected_idx >= (self.page + 1) * self.items_per_page:
                            self.page = self.selected_idx // self.items_per_page
                elif key == ord('\n') or key == curses.KEY_ENTER or key == 10 or key == 13:
                    self.launch_program()
                elif key == ord('n') or key == ord('N'):
                    self.next_page()
                elif key == ord('p') or key == ord('P'):
                    self.prev_page()
                elif key == curses.KEY_MOUSE:
                    try:
                        _, mouse_x, mouse_y, _, mouse_state = curses.getmouse()
                        if mouse_state & curses.BUTTON1_CLICKED:
                            self.handle_mouse(mouse_y, mouse_x)
                    except:
                        pass

            except KeyboardInterrupt:
                self.running = False


def main(stdscr):
    """Entry point for curses"""
    launcher = GUI_Launcher(stdscr)
    launcher.run()

    stdscr.clear()
    stdscr.addstr(0, 0, "Thank you for using GAMEZILLA MEGA COLLECTION!\n")
    stdscr.addstr(1, 0, "Press any key to exit...")
    stdscr.refresh()
    stdscr.getch()


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("\n")
        sys.exit(0)
