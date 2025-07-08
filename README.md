# 🧩 Sokoban Puzzle Solver with BFS and A* 🚀

This repository contains a Python implementation of the classic Sokoban puzzle game, enhanced with AI-powered solvers using **Breadth-First Search (BFS)** and **A\*** algorithms. A graphical interface built with **Pygame** allows users to visualize the puzzle and its solution in real time.

---

## 🎯 Objective

- Model the Sokoban puzzle in Python 🐍  
- Implement **BFS** and **A\*** search algorithms to solve the game  
- Detect and avoid deadlocks (corner traps, line blocks) to optimize search  
- Build an interactive **Pygame GUI** to play or watch the solution unfold  

---

## 📜 Game Rules

- 🎮 The player can move in four directions: `UP`, `DOWN`, `LEFT`, `RIGHT`  
- 📦 Boxes can only be **pushed**, not pulled  
- 🎯 The goal is to push all boxes onto the target spaces  
- 🚫 Deadlocks must be detected and avoided (e.g., boxes in corners or along walls)

---

## 🧠 Search Algorithms

### 🔍 Breadth-First Search (BFS)
- Explores all states level by level  
- **Guarantees shortest path**, but uses more memory on large maps  

### 💡 A\* Search
- Combines path cost with heuristics to guide the search  
- **Three heuristics** implemented:
  - `h1`: Number of boxes not on targets  
  - `h2`: `h1` + Manhattan distances from boxes to their nearest goals  
  - `h3`: A custom heuristic (you can define your own!)

---

## 🖼 Preview


| Game GUI | ![GUI](![Capture d'écran 2025-07-08 190714](https://github.com/user-attachments/assets/fdf07089-79f9-4192-bb9e-f5bc03b05d95)
(![Capture d'écran 2025-07-08 190730](https://github.com/user-attachments/assets/9e6e9930-edc3-45eb-9f86-f8511b9db94c)
)(![Capture d'écran 2025-07-08 190741](https://github.com/user-attachments/assets/d4fe3960-f6e5-4ba6-8b3d-ca7248a8173b)


---

## 🛠 Technologies

- Python 3.x  
- Pygame  
- Standard libraries: `collections`, `heapq`, etc.

---


## 🚀 Getting Started

1. Install dependencies:

```bash
pip install pygame

2- Run the solver:

python gui.py
