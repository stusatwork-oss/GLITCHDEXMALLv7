"""
HARD COPY ARCADE - PONG
A terminal-based Pong game that runs within the Eastland Mall.
Retro aesthetic. Simple controls. Endless nostalgia.
"""

import sys
import time
import random
import termios
import tty
import select

class PongGame:
    """Terminal-based Pong minigame for HARD COPY arcade."""

    # ANSI color codes
    RESET = "\033[0m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    WHITE = "\033[97m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    DIM = "\033[2m"
    BRIGHT = "\033[1m"

    def __init__(self, width=60, height=20):
        self.width = width
        self.height = height
        self.running = False

        # Paddle settings
        self.paddle_height = 4
        self.paddle_speed = 1

        # Player paddle (left)
        self.player_y = height // 2 - self.paddle_height // 2

        # AI paddle (right)
        self.ai_y = height // 2 - self.paddle_height // 2
        self.ai_speed = 0.7  # Slightly slower than ball for fairness

        # Ball
        self.ball_x = width // 2
        self.ball_y = height // 2
        self.ball_dx = random.choice([-1, 1])
        self.ball_dy = random.choice([-0.5, 0.5])

        # Scores
        self.player_score = 0
        self.ai_score = 0
        self.max_score = 5

        # Game state
        self.message = ""
        self.frame_count = 0

    def clear_screen(self):
        """Clear the terminal screen."""
        print("\033[2J\033[H", end="")

    def hide_cursor(self):
        """Hide the terminal cursor."""
        print("\033[?25l", end="")

    def show_cursor(self):
        """Show the terminal cursor."""
        print("\033[?25h", end="")

    def get_key(self):
        """Non-blocking key input."""
        if select.select([sys.stdin], [], [], 0)[0]:
            return sys.stdin.read(1)
        return None

    def draw_frame(self):
        """Draw the game frame."""
        self.clear_screen()

        # Create empty frame
        frame = [[' ' for _ in range(self.width)] for _ in range(self.height)]

        # Draw borders (top and bottom)
        for x in range(self.width):
            frame[0][x] = '='
            frame[self.height - 1][x] = '='

        # Draw center line
        for y in range(1, self.height - 1):
            if y % 2 == 0:
                frame[y][self.width // 2] = '|'

        # Draw player paddle (left)
        for i in range(self.paddle_height):
            py = int(self.player_y) + i
            if 0 < py < self.height - 1:
                frame[py][2] = '#'
                frame[py][3] = '#'

        # Draw AI paddle (right)
        for i in range(self.paddle_height):
            ay = int(self.ai_y) + i
            if 0 < ay < self.height - 1:
                frame[ay][self.width - 4] = '#'
                frame[ay][self.width - 3] = '#'

        # Draw ball
        bx = int(self.ball_x)
        by = int(self.ball_y)
        if 0 < by < self.height - 1 and 0 < bx < self.width - 1:
            frame[by][bx] = 'O'

        # Render frame
        print(f"{self.CYAN}{'=' * (self.width + 4)}{self.RESET}")
        print(f"{self.CYAN}= {self.BRIGHT}HARD COPY ARCADE - PONG{self.RESET}{self.CYAN}{' ' * (self.width - 23)}={self.RESET}")
        print(f"{self.CYAN}{'=' * (self.width + 4)}{self.RESET}")
        print()

        # Score display
        score_str = f"PLAYER: {self.player_score}  |  CPU: {self.ai_score}"
        padding = (self.width - len(score_str)) // 2
        print(f"{self.YELLOW}{' ' * padding}{score_str}{self.RESET}")
        print()

        # Draw game area
        for row in frame:
            line = ''.join(row)
            # Color the elements
            line = line.replace('#', f'{self.GREEN}#{self.RESET}')
            line = line.replace('O', f'{self.MAGENTA}O{self.RESET}')
            line = line.replace('|', f'{self.DIM}|{self.RESET}')
            print(f"  {line}")

        print()
        print(f"{self.DIM}  [W/S] Move paddle  |  [Q] Quit{self.RESET}")

        if self.message:
            print(f"\n{self.BRIGHT}{self.CYAN}  {self.message}{self.RESET}")

    def update_ball(self):
        """Update ball position and handle collisions."""
        # Move ball
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy

        # Top/bottom wall collision
        if self.ball_y <= 1:
            self.ball_y = 1
            self.ball_dy = abs(self.ball_dy)
        elif self.ball_y >= self.height - 2:
            self.ball_y = self.height - 2
            self.ball_dy = -abs(self.ball_dy)

        # Player paddle collision (left)
        if (self.ball_x <= 4 and
            self.player_y <= self.ball_y <= self.player_y + self.paddle_height):
            self.ball_dx = abs(self.ball_dx) * 1.05  # Slight speed increase
            # Add spin based on where ball hits paddle
            hit_pos = (self.ball_y - self.player_y) / self.paddle_height
            self.ball_dy = (hit_pos - 0.5) * 2

        # AI paddle collision (right)
        if (self.ball_x >= self.width - 5 and
            self.ai_y <= self.ball_y <= self.ai_y + self.paddle_height):
            self.ball_dx = -abs(self.ball_dx) * 1.05
            hit_pos = (self.ball_y - self.ai_y) / self.paddle_height
            self.ball_dy = (hit_pos - 0.5) * 2

        # Scoring
        if self.ball_x <= 0:
            self.ai_score += 1
            self.reset_ball()
        elif self.ball_x >= self.width - 1:
            self.player_score += 1
            self.reset_ball()

        # Cap ball speed
        max_speed = 2.0
        if abs(self.ball_dx) > max_speed:
            self.ball_dx = max_speed if self.ball_dx > 0 else -max_speed

    def reset_ball(self):
        """Reset ball to center after scoring."""
        self.ball_x = self.width // 2
        self.ball_y = self.height // 2
        self.ball_dx = random.choice([-1, 1])
        self.ball_dy = random.choice([-0.5, 0.5])

    def update_ai(self):
        """Simple AI that follows the ball."""
        paddle_center = self.ai_y + self.paddle_height // 2

        # Only move if ball is on AI's side
        if self.ball_x > self.width // 2:
            if paddle_center < self.ball_y - 1:
                self.ai_y += self.ai_speed
            elif paddle_center > self.ball_y + 1:
                self.ai_y -= self.ai_speed

        # Keep AI paddle in bounds
        if self.ai_y < 1:
            self.ai_y = 1
        if self.ai_y > self.height - self.paddle_height - 1:
            self.ai_y = self.height - self.paddle_height - 1

    def handle_input(self, key):
        """Handle player input."""
        if key == 'w' or key == 'W':
            self.player_y -= self.paddle_speed
        elif key == 's' or key == 'S':
            self.player_y += self.paddle_speed
        elif key == 'q' or key == 'Q':
            return False

        # Keep player paddle in bounds
        if self.player_y < 1:
            self.player_y = 1
        if self.player_y > self.height - self.paddle_height - 1:
            self.player_y = self.height - self.paddle_height - 1

        return True

    def check_winner(self):
        """Check if someone has won."""
        if self.player_score >= self.max_score:
            self.message = "YOU WIN! The arcade cabinet beeps approvingly."
            return True
        elif self.ai_score >= self.max_score:
            self.message = "CPU WINS. Insert another token to continue..."
            return True
        return False

    def run(self):
        """Main game loop."""
        # Save terminal settings
        old_settings = termios.tcgetattr(sys.stdin)

        try:
            # Set terminal to raw mode
            tty.setcbreak(sys.stdin.fileno())
            self.hide_cursor()

            self.running = True
            self.message = "First to 5 wins! Good luck..."

            while self.running:
                self.draw_frame()

                # Handle input
                key = self.get_key()
                if key:
                    if not self.handle_input(key):
                        break

                # Update game state
                self.update_ball()
                self.update_ai()

                # Check for winner
                if self.check_winner():
                    self.draw_frame()
                    time.sleep(2)
                    break

                # Frame rate control
                time.sleep(0.05)
                self.frame_count += 1

                # Clear message after a bit
                if self.frame_count > 60:
                    self.message = ""

        finally:
            # Restore terminal settings
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
            self.show_cursor()
            self.clear_screen()

        return self.player_score > self.ai_score


def play_pong():
    """Entry point for the Pong minigame."""
    print("\033[2J\033[H", end="")  # Clear screen

    print("\033[96m" + "=" * 50 + "\033[0m")
    print("\033[96m  HARD COPY ARCADE\033[0m")
    print("\033[96m" + "=" * 50 + "\033[0m")
    print()
    print("  The Pong cabinet glows invitingly.")
    print("  A single token slot. INSERT COIN.")
    print()
    print("\033[93m  [ENTER] Insert token and play\033[0m")
    print("\033[93m  [Q] Walk away\033[0m")
    print()

    choice = input("  > ").strip().lower()

    if choice == 'q':
        print("\n  You step back from the cabinet.")
        print("  It continues its soft electronic pinging.")
        time.sleep(1)
        return False

    # Play the game
    game = PongGame()
    won = game.run()

    # Post-game message
    print()
    if won:
        print("\033[92m  HIGH SCORE ACHIEVED\033[0m")
        print("  The cabinet dispenses... nothing.")
        print("  But you feel accomplished anyway.")
    else:
        print("\033[91m  GAME OVER\033[0m")
        print("  The cabinet resets, ready for the next player.")
        print("  There won't be one.")
    print()
    time.sleep(2)

    return won


if __name__ == "__main__":
    play_pong()
