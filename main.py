import tkinter as tk
import random
import time

# Grid settings
GRID_SIZE = 15  # Reduced from 20 to 15
CELL_SIZE = 30
DELAY = 0.1  # Delay between steps for visualization

# Colors
COLOR_EMPTY = "white"
COLOR_START = "green"
COLOR_TARGET = "red"
COLOR_FRONTIER = "yellow"
COLOR_EXPLORED = "lightblue"
COLOR_PATH = "purple"

class Node:
    def __init__(self, row, col, parent=None, cost=0):
        self.row = row
        self.col = col
        self.parent = parent
        self.cost = cost
    
    def __eq__(self, other):
        if other is None:
            return False
        return self.row == other.row and self.col == other.col
    
    def __hash__(self):
        return hash((self.row, self.col))

class PathfinderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Pathfinder - Uninformed Search")
        self.root.geometry("550x750")  # Fixed window size
        
        # Initialize grid
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.start = None
        self.target = None
        self.mode = "wall"
        self.is_running = False
        
        # Create canvas
        self.canvas = tk.Canvas(
            root, 
            width=GRID_SIZE * CELL_SIZE, 
            height=GRID_SIZE * CELL_SIZE,
            bg="white"
        )
        self.canvas.pack(pady=5)
        
        # Draw grid
        self.cells = {}
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x1 = col * CELL_SIZE
                y1 = row * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                cell = self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=COLOR_EMPTY,
                    outline="gray"
                )
                self.cells[(row, col)] = cell
        
        # Bind mouse click
        self.canvas.bind("<Button-1>", self.on_click)
        
        # Control panel
        control_frame = tk.Frame(root)
        control_frame.pack(pady=5)
        
        # Mode buttons
        tk.Button(control_frame, text="Set Start", width=10, height=1,
                 bg="green", fg="white", font=("Arial", 9, "bold"),
                 command=lambda: self.set_mode("start")).grid(row=0, column=0, padx=3)
        tk.Button(control_frame, text="Set Target", width=10, height=1,
                 bg="red", fg="white", font=("Arial", 9, "bold"),
                 command=lambda: self.set_mode("target")).grid(row=0, column=1, padx=3)
        tk.Button(control_frame, text="Clear Grid", width=10, height=1,
                 bg="orange", fg="black", font=("Arial", 9, "bold"),
                 command=self.clear_grid).grid(row=0, column=3, padx=3)
        
        # Algorithm buttons section
        tk.Label(root, text="══ Select Search Algorithm ══", 
                font=("Arial", 11, "bold"), bg="lightgray", relief=tk.RIDGE).pack(pady=5, fill=tk.X, padx=20)
        
        algo_frame = tk.Frame(root, bg="white")
        algo_frame.pack(pady=5)
        
        tk.Button(algo_frame, text="BFS", width=13, height=2,
                 bg="#90EE90", fg="black", font=("Arial", 9, "bold"),
                 relief=tk.RAISED, bd=3,
                 command=lambda: self.run_algorithm("BFS")).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(algo_frame, text="DFS", width=13, height=2,
                 bg="#FFB6C1", fg="black", font=("Arial", 9, "bold"),
                 relief=tk.RAISED, bd=3,
                 command=lambda: self.run_algorithm("DFS")).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(algo_frame, text="UCS", width=13, height=2,
                 bg="#FFFFE0", fg="black", font=("Arial", 9, "bold"),
                 relief=tk.RAISED, bd=3,
                 command=lambda: self.run_algorithm("UCS")).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(algo_frame, text="DLS", width=13, height=2,
                 bg="#ADD8E6", fg="black", font=("Arial", 9, "bold"),
                 relief=tk.RAISED, bd=3,
                 command=lambda: self.run_algorithm("DLS")).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(algo_frame, text="IDDFS", width=13, height=2,
                 bg="#DDA0DD", fg="black", font=("Arial", 9, "bold"),
                 relief=tk.RAISED, bd=3,
                 command=lambda: self.run_algorithm("IDDFS")).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(algo_frame, text="Bidirectional", width=13, height=2,
                 bg="#FFDAB9", fg="black", font=("Arial", 9, "bold"),
                 relief=tk.RAISED, bd=3,
                 command=lambda: self.run_algorithm("Bidirectional")).grid(row=1, column=2, padx=5, pady=5)
        
        # Status label
        self.status_label = tk.Label(root, text="Click to set start point", 
                                    font=("Arial", 10), bg="lightyellow", relief=tk.SUNKEN)
        self.status_label.pack(pady=5, fill=tk.X, padx=20)
    
    def set_mode(self, mode):
        self.mode = mode
        if mode == "start":
            self.status_label.config(text="Click to set start point")
        elif mode == "target":
            self.status_label.config(text="Click to set target point")
        elif mode == "wall":
            self.status_label.config(text="Click to draw walls")
    
    def on_click(self, event):
        if self.is_running:
            return
        
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE
        
        if row < 0 or row >= GRID_SIZE or col < 0 or col >= GRID_SIZE:
            return
        
        if self.mode == "start":
            if self.start:
                old_row, old_col = self.start
                self.grid[old_row][old_col] = 0
                self.update_cell(old_row, old_col, COLOR_EMPTY)
            self.start = (row, col)
            self.grid[row][col] = 0
            self.update_cell(row, col, COLOR_START)
            self.status_label.config(text="Start point set. Now set target point.")
            
        elif self.mode == "target":
            if self.target:
                old_row, old_col = self.target
                self.grid[old_row][old_col] = 0
                self.update_cell(old_row, old_col, COLOR_EMPTY)
            self.target = (row, col)
            self.grid[row][col] = 0
            self.update_cell(row, col, COLOR_TARGET)
            self.status_label.config(text="Target point set. Choose algorithm to run.")

    def update_cell(self, row, col, color):
        self.canvas.itemconfig(self.cells[(row, col)], fill=color)
        self.root.update()
    
    def clear_grid(self):
        if self.is_running:
            return
        
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.start = None
        self.target = None
        
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                self.update_cell(row, col, COLOR_EMPTY)
        
        self.status_label.config(text="Grid cleared. Set start point.")
    
    def reset_visualization(self):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if (row, col) == self.start:
                    self.update_cell(row, col, COLOR_START)
                elif (row, col) == self.target:
                    self.update_cell(row, col, COLOR_TARGET)
                else:
                    self.update_cell(row, col, COLOR_EMPTY)
    
    def run_algorithm(self, algo_name):
        if not self.start or not self.target:
            self.status_label.config(text="Please set both start and target points!")
            return

        algo_map = {
            "BFS":           self.bfs,
            "DFS":           self.dfs,
            "UCS":           self.ucs,
            "DLS":           lambda: self.dls(15),
            "IDDFS":         self.iddfs,
            "Bidirectional": self.bidirectional,
        }

        self.is_running = True
        self.reset_visualization()
        self.status_label.config(text=f"Running {algo_name}...")

        path = algo_map[algo_name]()

        self.status_label.config(text=
            f"{algo_name} found path! Length: {len(path)}" if path else
            f"{algo_name} - No path found!"
        )
        self.visualize_path(path) if path else None
        self.is_running = False    
        

    def get_neighbors(self, node):
        DIRECTIONS = [(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]
        #here (-1,0) is up, (-1,1) is top-right diagonal, (0,1) is right
        #(1,1) is bottom-right diagonal, (1,0)is bottom
        #(1,-1) is bottom-left diagonal, (0,-1)is left
        #(-1,-1) top-left diagonal
        return [
            Node(node.row + dr, node.col + dc, node,
                node.cost + (1.4 if dr and dc else 1.0))
            for dr, dc in DIRECTIONS
            if 0 <= node.row + dr < GRID_SIZE
            and 0 <= node.col + dc < GRID_SIZE
            and self.grid[node.row + dr][node.col + dc] ==0
        ]
    
    def bfs(self):
        from collections import deque
        frontier = deque([Node(*self.start)])
        explored = set()
        frontier_set = {self.start}

        while frontier:
            current = frontier.popleft()
            pos = (current.row, current.col)

            explored.add(pos)
            frontier_set.discard(pos)
            if pos not in (self.start, self.target):
                self.update_cell(*pos, COLOR_EXPLORED)
                time.sleep(DELAY)

            if pos == self.target:
                return self.reconstruct_path(current)

            for neighbor in self.get_neighbors(current):
                npos = (neighbor.row, neighbor.col)
                if npos not in explored and npos not in frontier_set:
                    frontier.append(neighbor)
                    frontier_set.add(npos)
                    if npos != self.target:
                        self.update_cell(*npos, COLOR_FRONTIER)

        return None
    
    def dfs(self):
        frontier = [Node(*self.start)]
        explored = set()

        while frontier:
            current = frontier.pop()
            pos = (current.row, current.col)

            if pos in explored:
                continue

            explored.add(pos)
            if pos not in (self.start, self.target):
                self.update_cell(*pos, COLOR_EXPLORED)
                time.sleep(DELAY)

            if pos == self.target:
                return self.reconstruct_path(current)

            for neighbor in reversed(self.get_neighbors(current)):
                npos = (neighbor.row, neighbor.col)
                if npos not in explored:
                    frontier.append(neighbor)
                    if npos != self.target:
                        self.update_cell(*npos, COLOR_FRONTIER)

        return None
    def ucs(self):
        import heapq
        frontier = [(0, Node(*self.start))]
        explored = set()
        cost_map = {self.start: 0}

        while frontier:
            _, current = heapq.heappop(frontier)
            pos = (current.row, current.col)

            if pos in explored:
                continue

            explored.add(pos)
            if pos not in (self.start, self.target):
                self.update_cell(*pos, COLOR_EXPLORED)
                time.sleep(DELAY)

            if pos == self.target:
                return self.reconstruct_path(current)

            for neighbor in self.get_neighbors(current):
                npos = (neighbor.row, neighbor.col)
                if npos not in explored and neighbor.cost < cost_map.get(npos, float('inf')):
                    cost_map[npos] = neighbor.cost
                    heapq.heappush(frontier, (neighbor.cost, neighbor))
                    if npos != self.target:
                        self.update_cell(*npos, COLOR_FRONTIER)

        return None
    def dls_recursive(self, node, target, limit, explored):
        """Depth-Limited Search recursive helper"""
        if limit < 0:
            return None
        
        explored.add((node.row, node.col))
        if (node.row, node.col) != self.start and (node.row, node.col) != self.target:
            self.update_cell(node.row, node.col, COLOR_EXPLORED)
            time.sleep(DELAY)
        
        # Check if goal
        if node.row == target.row and node.col == target.col:
            return self.reconstruct_path(node)
        
        # Expand neighbors
        for neighbor in self.get_neighbors(node):
            neighbor_pos = (neighbor.row, neighbor.col)
            
            if neighbor_pos not in explored:
                if neighbor_pos != self.target:
                    self.update_cell(neighbor.row, neighbor.col, COLOR_FRONTIER)
                
                result = self.dls_recursive(neighbor, target, limit - 1, explored)
                if result:
                    return result
        
        return None
    
    def dls(self, depth_limit):
        """Depth-Limited Search"""
        start_node = Node(self.start[0], self.start[1])
        target_node = Node(self.target[0], self.target[1])
        explored = set()
        
        return self.dls_recursive(start_node, target_node, depth_limit, explored)
    
    def iddfs(self):
        """Iterative Deepening Depth-First Search"""
        max_depth = GRID_SIZE * 2  # Maximum possible depth
        
        for depth in range(max_depth):
            self.reset_visualization()
            self.status_label.config(text=f"IDDFS - Trying depth: {depth}")
            
            start_node = Node(self.start[0], self.start[1])
            target_node = Node(self.target[0], self.target[1])
            explored = set()
            
            result = self.dls_recursive(start_node, target_node, depth, explored)
            if result:
                return result
        
        return None
    
    def bidirectional(self):
        """Bidirectional Search"""
        start_node = Node(self.start[0], self.start[1])
        target_node = Node(self.target[0], self.target[1])
        
        # Forward search from start
        frontier_forward = [start_node]
        explored_forward = {}
        explored_forward[(start_node.row, start_node.col)] = start_node
        
        # Backward search from target
        frontier_backward = [target_node]
        explored_backward = {}
        explored_backward[(target_node.row, target_node.col)] = target_node
        
        while frontier_forward and frontier_backward:
            
            if frontier_forward:
                current_f = frontier_forward[0]
                frontier_forward = frontier_forward[1:]
                
                pos_f = (current_f.row, current_f.col)
                if pos_f != self.start and pos_f != self.target:
                    self.update_cell(current_f.row, current_f.col, COLOR_EXPLORED)
                    time.sleep(DELAY / 2)
                
                if pos_f in explored_backward:
                    return self.merge_paths(current_f, explored_backward[pos_f])
                
                for neighbor in self.get_neighbors(current_f):
                    neighbor_pos = (neighbor.row, neighbor.col)
                    
                    if neighbor_pos not in explored_forward:
                        explored_forward[neighbor_pos] = neighbor
                        frontier_forward.append(neighbor)
                        if neighbor_pos != self.target and neighbor_pos not in explored_backward:
                            self.update_cell(neighbor.row, neighbor.col, COLOR_FRONTIER)
            
            if frontier_backward:
                current_b = frontier_backward[0]
                frontier_backward = frontier_backward[1:]
                
                pos_b = (current_b.row, current_b.col)
                if pos_b != self.start and pos_b != self.target:
                    self.update_cell(current_b.row, current_b.col, COLOR_EXPLORED)
                    time.sleep(DELAY / 2)
                
                if pos_b in explored_forward:
                    return self.merge_paths(explored_forward[pos_b], current_b)
                
                for neighbor in self.get_neighbors(current_b):
                    neighbor_pos = (neighbor.row, neighbor.col)
                    
                    if neighbor_pos not in explored_backward:
                        explored_backward[neighbor_pos] = neighbor
                        frontier_backward.append(neighbor)
                        if neighbor_pos != self.start and neighbor_pos not in explored_forward:
                            self.update_cell(neighbor.row, neighbor.col, COLOR_FRONTIER)
        
        return None
    
    def merge_paths(self, forward_node, backward_node):
        """Merge paths from bidirectional search"""
        path1 = []
        current = forward_node
        while current:
            path1.append((current.row, current.col))
            current = current.parent
        path1.reverse()
        
        path2 = []
        current = backward_node.parent
        while current:
            path2.append((current.row, current.col))
            current = current.parent
        
        return path1 + path2
    
    def reconstruct_path(self, node):
        """Reconstruct path from goal to start"""
        path = []
        current = node
        while current:
            path.append((current.row, current.col))
            current = current.parent
        path.reverse()
        return path
    
    def visualize_path(self, path):
        """Visualize the final path"""
        for row, col in path:
            if (row, col) != self.start and (row, col) != self.target:
                self.update_cell(row, col, COLOR_PATH)
                time.sleep(DELAY / 2)

if __name__ == "__main__":
    root = tk.Tk()
    app = PathfinderGUI(root)
    root.mainloop()
