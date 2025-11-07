# 🎮 Grid Game (Tkinter Version)

A simple but fun **grid-based game** built with **Python and Tkinter**, featuring:
- Multiple difficulty modes  
- Keyboard controls (WASD / Arrow Keys)  
- Persistent high-score tracking  
- Smooth GUI updates  
- A clean main menu interface  

This project was developed as part of the **Foundations of Programming and Software Engineering** coursework (Assessment 2).

---

## 🧩 Features

| Feature | Description |
|----------|--------------|
| 🎯 **Goal** | Reach the green goal cell (`G`) while avoiding enemies (`E`). |
| 🧍 **Player** | Represented by a red cell (`P`), moves using **W/A/S/D** or **arrow keys**. |
| 💀 **Enemies** | Blue cells that reduce your health by 10 points if you collide with them. |
| ❤️ **Health System** | Starts at 100, decreases each move (based on difficulty). |
| ⚙️ **Difficulties** | Easy / Medium / Hard, affecting enemy count and move cost. |
| 🏆 **High Scores** | Stored persistently in `/leaderboard/high_scores.json`. |
| 🪄 **Smooth Rendering** | Grid refreshes seamlessly — no flickering. |
| 🖱️ **GUI Menu** | Start Game, Set Difficulty, View High Scores, Quit. |

---

## 🖥️ Requirements

Before running the game, ensure you have:

- **Python 3.8+** installed  
- **Tkinter** (usually pre-installed with Python)  

You can verify Tkinter installation with:
```bash
python -m tkinter
````

If it opens a blank window, you're good to go!

If Tkinter isn’t installed:

* **Windows / macOS:** Reinstall Python from [python.org/downloads](https://www.python.org/downloads/)
* **Linux (Debian/Ubuntu):**

  ```bash
  sudo apt-get install python3-tk
  ```

---

## 🚀 How to Run

1. **Clone this repository**:

   ```bash
   git clone https://github.com/Zainbil/keele.git
   ```

2. **Run the game**:

   ```bash
   python main.py
   ```

3. **Play using keyboard:**

   * **W / ↑** → Move Up
   * **S / ↓** → Move Down
   * **A / ←** → Move Left
   * **D / →** → Move Right

---

## 🏁 Gameplay Overview

1. Start the game from the main menu.
2. Choose your difficulty (Easy / Medium / Hard).
3. Move around the grid to reach the **green goal**.
4. Avoid **blue enemies** — they reduce your health!
5. Each move costs energy based on difficulty level.
6. Your **final score** equals your **remaining health**.
7. High scores are saved automatically by difficulty level.

---

## 💾 Leaderboard File

The game automatically creates and updates:

```
leaderboard/
 └── high_scores.json
```

Example structure:

```json
{
  "Easy": 85,
  "Medium": 60,
  "Hard": 30
}
```

---

## ⚙️ Project Structure

```
📁 grid-game/
│
├── grid_game_gui.py          # Main Tkinter game script
├── leaderboard/
│   └── high_scores.json      # Auto-generated high score data
└── README.md                 # This file
```

---

## 💡 Developer Notes

* The GUI grid updates **seamlessly**, using `.config()` instead of recreating labels each frame.
* Keyboard input is handled via **Tkinter event bindings**.
* The game supports both **WASD** and **arrow keys** for movement.
* All data (like scores) is stored locally — no internet connection required.

---

## 🧠 Acknowledgment

```python
# I acknowledge the use of OpenAI ChatGPT (GPT-5, https://chat.openai.com)
# for assisting in designing, optimizing, and implementing keyboard controls,
# seamless grid refresh, and GUI improvements for this Tkinter version.
```

---

## 📚 Version History

| Iteration | Description                                                       |
| --------- | ----------------------------------------------------------------- |
| 1️⃣       | Basic grid and movement (console)                                 |
| 2️⃣       | Added enemies and health system                                   |
| 3️⃣       | Introduced difficulty settings and move cost                      |
| 4️⃣       | Added persistent leaderboard and color-coded grid                 |
| 5️⃣       | Converted to Tkinter GUI with keyboard control and smooth updates |

---

## 🧑‍💻 Author

**Zain**
*Foundations of Programming and Software Engineering (CSC-44102)*

Keele University

📧 Y5d93@students.keele.ac.uk

---

Enjoy the game — and good luck reaching the goal! 🎯

