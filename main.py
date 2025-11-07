# I acknowledge the use of OpenAI ChatGPT (GPT-5, https://chat.openai.com)
# for assisting in structuring and debugging this Tkinter GUI version of Grid Game.

import tkinter as tk
from tkinter import messagebox
import random
import json
import os

class GridGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Grid Game")
        self.size = 8
        self.health = 100
        self.score = 0
        self.difficulty = "Medium"
        self.settings = {
            'Easy': {'enemy_count': 4, 'move_cost': 1},
            'Medium': {'enemy_count': 7, 'move_cost': 2},
            'Hard': {'enemy_count': 10, 'move_cost': 3},
        }
        self.leaderboard_dir = "leaderboard"
        self.leaderboard_file = os.path.join(self.leaderboard_dir, "high_scores.json")

        # Keep track of all active frames
        self.frames = []

        # Start with main menu
        self.show_main_menu()

    # --- FRAME MANAGEMENT ---
    def clear_frames(self):
        """Destroy all frames to prevent stacking."""
        for f in self.frames:
            f.destroy()
        self.frames.clear()

    # --- MAIN MENU ---
    def show_main_menu(self):
        self.clear_frames()
        frame_menu = tk.Frame(self.root)
        self.frames.append(frame_menu)
        frame_menu.pack(pady=50)

        tk.Label(frame_menu, text="🎲 GRID GAME", font=("Arial", 20, "bold")).pack(pady=15)
        tk.Button(frame_menu, text="▶ Start Game", width=20, height=2, command=self.start_game).pack(pady=5)
        tk.Button(frame_menu, text="⚙ Set Difficulty", width=20, height=2, command=self.set_difficulty).pack(pady=5)
        tk.Button(frame_menu, text="🏆 View High Scores", width=20, height=2, command=self.show_high_scores).pack(pady=5)
        tk.Button(frame_menu, text="❌ Quit", width=20, height=2, command=self.root.quit).pack(pady=5)

    # --- GAMEPLAY ---
    def start_game(self):
        self.clear_frames()
        self.health = 100
        self.score = 0
        self.game_over = False

        frame_top = tk.Frame(self.root)
        frame_top.pack(pady=10)
        self.frames.append(frame_top)

        self.label_info = tk.Label(frame_top, text=f"Difficulty: {self.difficulty} | ❤️ Health: {self.health}", font=("Arial", 12))
        self.label_info.pack()

        frame_game = tk.Frame(self.root)
        frame_game.pack()
        self.frames.append(frame_game)
        self.frame_game = frame_game

        frame_controls = tk.Frame(self.root)
        frame_controls.pack(pady=10)
        self.frames.append(frame_controls)
        self.create_control_buttons(frame_controls)

        # Setup positions
        all_positions = [(i, j) for i in range(self.size) for j in range(self.size)]
        self.goal_pos = random.choice(all_positions)
        self.player_pos = random.choice([pos for pos in all_positions if pos != self.goal_pos])
        exclude = {self.goal_pos, self.player_pos}
        self.enemy_positions = random.sample([pos for pos in all_positions if pos not in exclude],
                                             self.settings[self.difficulty]['enemy_count'])

        self.draw_grid()
        self.update_info_label()

    def create_control_buttons(self, frame):
        tk.Button(frame, text="↑", width=5, command=lambda: self.move_player('W')).grid(row=0, column=1)
        tk.Button(frame, text="←", width=5, command=lambda: self.move_player('A')).grid(row=1, column=0)
        tk.Button(frame, text="↓", width=5, command=lambda: self.move_player('S')).grid(row=1, column=1)
        tk.Button(frame, text="→", width=5, command=lambda: self.move_player('D')).grid(row=1, column=2)
        tk.Button(frame, text="🏠 Menu", width=10, command=self.show_main_menu).grid(row=2, column=1, pady=5)

    def draw_grid(self):
        for widget in self.frame_game.winfo_children():
            widget.destroy()

        for i in range(self.size):
            for j in range(self.size):
                cell_text = ""
                bg_color = "lightgrey"

                if (i, j) == self.player_pos:
                    cell_text = "P"
                    bg_color = "red"
                elif (i, j) == self.goal_pos:
                    cell_text = "G"
                    bg_color = "green"
                elif (i, j) in self.enemy_positions:
                    cell_text = "E"
                    bg_color = "skyblue"

                label = tk.Label(self.frame_game, text=cell_text, width=4, height=2,
                                 font=("Arial", 10, "bold"), bg=bg_color, relief="ridge")
                label.grid(row=i, column=j, padx=1, pady=1)

    def move_player(self, direction):
        if getattr(self, "game_over", False):
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

        new_x = max(0, min(self.size - 1, self.player_pos[0] + dx))
        new_y = max(0, min(self.size - 1, self.player_pos[1] + dy))
        self.player_pos = (new_x, new_y)

        self.health -= self.settings[self.difficulty]['move_cost']

        if self.player_pos in self.enemy_positions:
            self.health -= 10
            messagebox.showinfo("Hit!", "⚔️ You hit an enemy! -10 health")
        elif self.player_pos == self.goal_pos:
            self.score = self.health
            self.game_over = True
            self.update_high_score()
            messagebox.showinfo("🎉 Victory!", f"You reached the goal!\nFinal Score: {self.score}")
            self.show_main_menu()
            return

        if self.health <= 0:
            self.health = 0
            self.game_over = True
            messagebox.showwarning("💀 Game Over", "You ran out of health!")
            self.show_main_menu()
            return

        self.update_info_label()
        self.draw_grid()

    def update_info_label(self):
        self.label_info.config(text=f"Difficulty: {self.difficulty} | ❤️ Health: {self.health}")

    # --- LEADERBOARD ---
    def read_high_scores(self):
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
        scores = self.read_high_scores()
        prev_score = scores.get(self.difficulty, 0)
        if self.score > prev_score:
            scores[self.difficulty] = self.score
            with open(self.leaderboard_file, 'w') as f:
                json.dump(scores, f)
            messagebox.showinfo("🏆 High Score!", f"New high score for {self.difficulty}: {self.score}")
        else:
            messagebox.showinfo("Score", f"Your score: {self.score}\nCurrent high score: {prev_score}")

    def show_high_scores(self):
        scores = self.read_high_scores()
        text = "\n".join([f"{k}: {v}" for k, v in scores.items()])
        messagebox.showinfo("🏆 High Scores", text)

    # --- SETTINGS ---
    def set_difficulty(self):
        diff_win = tk.Toplevel(self.root)
        diff_win.title("Select Difficulty")
        tk.Label(diff_win, text="Choose Difficulty", font=("Arial", 12, "bold")).pack(pady=5)
        for diff in ["Easy", "Medium", "Hard"]:
            tk.Button(diff_win, text=diff, width=10, command=lambda d=diff: self.change_difficulty(d, diff_win)).pack(pady=3)

    def change_difficulty(self, diff, window):
        self.difficulty = diff
        window.destroy()
        messagebox.showinfo("Difficulty Set", f"Difficulty changed to {diff}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GridGameGUI(root)
    root.mainloop()
