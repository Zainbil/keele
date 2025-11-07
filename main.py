# I acknowledge the use of OpenAI ChatGPT (GPT-5, https://chat.openai.com)
# to assist in structuring and writing this iteration of the Grid Game.

import os
import random

class GridGame:
    def __init__(self, size=8, enemy_count=5):
        self.size = size
        self.enemy_count = enemy_count
        self.health = 100
        self.game_over = False
        self.player_pos = self.random_position()
        self.goal_pos = self.random_position(exclude=[self.player_pos])
        self.enemy_positions = self.generate_enemies()
        self.grid = []
        self.update_grid()

    def random_position(self, exclude=None):
        exclude = exclude or []
        while True:
            pos = (random.randint(0, self.size - 1), random.randint(0, self.size - 1))
            if pos not in exclude:
                return pos

    def generate_enemies(self):
        positions = set()
        exclude = {self.player_pos, self.goal_pos}
        while len(positions) < self.enemy_count:
            pos = self.random_position(exclude=list(exclude))
            positions.add(pos)
            exclude.add(pos)
        return list(positions)

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def update_grid(self):
        self.grid = [['#' for _ in range(self.size)] for _ in range(self.size)]
        # Place goal
        gx, gy = self.goal_pos
        self.grid[gx][gy] = 'G'
        # Place enemies
        for ex, ey in self.enemy_positions:
            self.grid[ex][ey] = 'E'
        # Place player
        px, py = self.player_pos
        self.grid[px][py] = 'P'

    def display_health_bar(self, width=20):
        ratio = self.health / 100
        filled = int(width * ratio)
        bar = '█' * filled + '-' * (width - filled)
        color = "\033[92m" if ratio > 0.5 else "\033[93m" if ratio > 0.2 else "\033[91m"
        return f"[{color}{bar}\033[0m] {self.health}/100"

    def print_grid(self):
        self.clear_screen()
        print("=== GRID GAME ===")
        print("Use W/A/S/D to move. Reach G, avoid E.\n")
        print("❤️ Health:", self.display_health_bar(), "\n")
        for row in self.grid:
            print(' '.join(row))
        if self.game_over:
            if self.health <= 0:
                print("\n💀 Game Over! You ran out of health!")
            else:
                print("\n🎉 You reached the goal!")

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

        # Check collisions
        if self.player_pos in self.enemy_positions:
            self.health -= 20
            print("\n⚔️ You hit an enemy! -20 health.")
        elif self.player_pos == self.goal_pos:
            self.game_over = True
            return

        if self.health <= 0:
            self.health = 0
            self.game_over = True

        self.update_grid()

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

if __name__ == "__main__":
    game = GridGame()
    game.play()
