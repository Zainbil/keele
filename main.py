# I acknowledge the use of OpenAI ChatGPT (GPT-5, https://chat.openai.com)
# for assisting with code organization, leaderboard persistence, and visual formatting.

import os
import sys
import json
import random

class GridGame:
    def __init__(self, size=8, difficulty='Medium'):
        self.size = size
        self.difficulty = difficulty
        self.settings = {
            'Easy': {'enemy_count': 4, 'move_cost': 1},
            'Medium': {'enemy_count': 7, 'move_cost': 2},
            'Hard': {'enemy_count': 10, 'move_cost': 3}
        }
        self.health = 100
        self.game_over = False
        self.score = 0
        self.goal_pos = None
        self.player_pos = None
        self.enemy_positions = []
        self.grid = []
        self.leaderboard_dir = "leaderboard"
        self.leaderboard_file = os.path.join(self.leaderboard_dir, "high_scores.json")
        self.init_positions()
        self.update_grid()

    def init_positions(self):
        all_positions = [(i, j) for i in range(self.size) for j in range(self.size)]
        self.goal_pos = random.choice(all_positions)
        self.player_pos = random.choice([pos for pos in all_positions if pos != self.goal_pos])
        exclude = {self.goal_pos, self.player_pos}
        self.enemy_positions = random.sample([pos for pos in all_positions if pos not in exclude],
                                             self.settings[self.difficulty]['enemy_count'])

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def update_grid(self):
        self.grid = [['#' for _ in range(self.size)] for _ in range(self.size)]
        # Place goal (green)
        gx, gy = self.goal_pos
        self.grid[gx][gy] = '\033[92mG\033[0m'
        # Place enemies (blue)
        for ex, ey in self.enemy_positions:
            self.grid[ex][ey] = '\033[94mE\033[0m'
        # Place player (red)
        px, py = self.player_pos
        self.grid[px][py] = '\033[91mP\033[0m'

    def display_health_bar(self, width=20):
        ratio = self.health / 100
        filled = int(width * ratio)
        bar = '█' * filled + '-' * (width - filled)
        color = "\033[92m" if ratio > 0.5 else "\033[93m" if ratio > 0.2 else "\033[91m"
        return f"[{color}{bar}\033[0m] {self.health}/100"

    def print_grid(self):
        self.clear_screen()
        print(f"=== GRID GAME ===   🎮 Difficulty: {self.difficulty}")
        print("Use W/A/S/D to move. Reach G, avoid E.\n")
        print("❤️ Health:", self.display_health_bar(), "\n")
        for row in self.grid:
            print(' '.join(row))
        if self.game_over:
            if self.health <= 0:
                print("\n💀 Game Over! You ran out of health!")
            elif self.health > 0:
                print("\n🎉 Congratulations! You reached the goal!")
                print(f"🏆 Final Score: {self.health}")
                self.score = self.health
                self.update_high_score()

    def move_player(self, direction):
        if self.game_over:
            return

        dx, dy = 0, 0
        if direction == 'W':
            dx = -1
        elif direction == 'S':
            dx = 1
        elif direction == 'A':
            dy = -1
        elif direction == 'D':
            dy = 1
        else:
            return

        new_x = max(0, min(self.size - 1, self.player_pos[0] + dx))
        new_y = max(0, min(self.size - 1, self.player_pos[1] + dy))
        self.player_pos = (new_x, new_y)

        # Deduct movement cost
        self.health -= self.settings[self.difficulty]['move_cost']

        # Collision checks
        if self.player_pos in self.enemy_positions:
            self.health -= 10
            print("\n⚔️ You hit an enemy! -10 health.")
        elif self.player_pos == self.goal_pos:
            self.game_over = True
            return

        if self.health <= 0:
            self.health = 0
            self.game_over = True

        self.update_grid()

    def read_high_scores(self):
        """Read existing scores or return defaults."""
        if not os.path.exists(self.leaderboard_dir):
            os.makedirs(self.leaderboard_dir)
        if not os.path.exists(self.leaderboard_file):
            return {'Easy': 0, 'Medium': 0, 'Hard': 0}

        try:
            with open(self.leaderboard_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {'Easy': 0, 'Medium': 0, 'Hard': 0}

    def update_high_score(self):
        """Save new high score if it beats the previous one."""
        scores = self.read_high_scores()
        prev_score = scores.get(self.difficulty, 0)
        if self.score > prev_score:
            scores[self.difficulty] = self.score
            with open(self.leaderboard_file, 'w') as f:
                json.dump(scores, f)
            print(f"\n🎉 New High Score for {self.difficulty}: {self.score}")
        else:
            print(f"\nYour score: {self.score} | Current high score: {prev_score}")

    def play(self):
        while not self.game_over:
            self.print_grid()
            move = input("\nMove (W/A/S/D or Q to quit): ").upper()
            if move == 'Q':
                print("👋 Exiting game.")
                break
            self.move_player(move)

        self.print_grid()
        print("\nThanks for playing!")


def show_high_scores():
    """Display all saved high scores."""
    game = GridGame()
    scores = game.read_high_scores()
    print("\n=== 🏆 HIGH SCORES ===")
    for diff, score in scores.items():
        print(f"{diff}: {score}")
    input("\nPress Enter to return to menu...")


def main_menu():
    global selected_difficulty
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("==== 🎲 GRID GAME ====")
        print("1. Start Game")
        print("2. Set Difficulty")
        print("3. View High Scores")
        print("4. Quit")
        choice = input("\nSelect option (1-4): ")

        if choice == '1':
            return selected_difficulty
        elif choice == '2':
            difficulty = input("Choose difficulty (Easy / Medium / Hard): ").capitalize()
            if difficulty in ['Easy', 'Medium', 'Hard']:
                selected_difficulty = difficulty
                print(f"Difficulty set to {difficulty}")
                input("Press Enter to return to menu...")
            else:
                print("Invalid difficulty. Press Enter to continue...")
                input()
        elif choice == '3':
            show_high_scores()
        elif choice == '4':
            print("👋 Goodbye!")
            sys.exit()
        else:
            print("Invalid input! Press Enter to continue...")
            input()


# Default difficulty
selected_difficulty = 'Medium'

if __name__ == "__main__":
    selected_difficulty = main_menu()
    game = GridGame(difficulty=selected_difficulty)
    game.play()
