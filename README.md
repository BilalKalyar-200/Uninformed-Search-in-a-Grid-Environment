# AI Pathfinder - Uninformed Search Visualizer

## Dependencies

This project uses **only Python built-in libraries**:
- `tkinter` — GUI (comes pre-installed with Python)
- `time` — step delays for visualization (built-in)

> No `pip install` is needed.

---

## Requirements

- Python **3.6 or higher**

To check your Python version:
```bash
python --version
```

---

## How to Run

### Step 1 — Download the file
Save `pathfinder.py` to any folder on your computer.

### Step 2 — Open a terminal in that folder

**Windows:**
```
Win + R → type cmd → navigate to folder with cd
```
**Mac / Linux:**
```
Open Terminal → navigate to folder with cd
```

### Step 3 — Run the script
```bash
python pathfinder.py
```

---

## If tkinter is Missing

tkinter ships with Python by default, but on some Linux systems it needs a separate install:

**Ubuntu / Debian:**
```bash
sudo apt-get install python3-tk
```

**Fedora:**
```bash
sudo dnf install python3-tkinter
```

**Mac (Homebrew Python):**
```bash
brew install python-tk
```

---

## How to Use the App

### 1. Place Start and Target
- Click **Set Start** → click any cell on the grid (turns green)
- Click **Set Target** → click any cell on the grid (turns red)

### 2. Run an Algorithm
Click any of the 6 algorithm buttons:

| Button        | Algorithm                  | Behavior                              |
|---------------|----------------------------|---------------------------------------|
| BFS           | Breadth-First Search       | Explores level by level               |
| DFS           | Depth-First Search         | Goes deep before going wide           |
| UCS           | Uniform-Cost Search        | Expands by lowest path cost           |
| DLS           | Depth-Limited Search       | DFS with a depth cap of 15            |
| IDDFS         | Iterative Deepening DFS    | Repeats DLS with increasing depth     |
| Bidirectional | Bidirectional Search       | Searches from both ends at once       |

### 3. Watch the Visualization

| Color       | Meaning                          |
|-------------|----------------------------------|
| 🟢 Green    | Start point                      |
| 🔴 Red      | Target point                     |
| 🟡 Yellow   | Frontier — waiting to be explored|
| 🔵 Blue     | Explored — already visited       |
| 🟣 Purple   | Final path found                 |

### 4. Reset
Click **Clear Grid** to wipe the board and start over.

---

## Movement Rules

The agent can move in all **8 directions** (clockwise order):

```
Up → Top-Right → Right → Bottom-Right → Bottom → Bottom-Left → Left → Top-Left
```

- Straight move cost: **1.0**
- Diagonal move cost: **1.4**
