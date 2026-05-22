# ids1.py - Thuật toán Tìm kiếm sâu dần (IDS) - Tiếp cận 1 (Late Test)
class Node:
    def __init__(self, state, parent, action, depth):
        self.state = state  # state: (robot_r, robot_c, grid_tuple)
        self.parent = parent
        self.action = action
        self.depth = depth

def is_goal(state):
    grid = state[2]
    return sum(sum(row) for row in grid) == 0

def get_children(node):
    rx, ry, grid = node.state
    children = []
    # Thứ tự sinh con ưu tiên: Phải -> Xuống -> Trái -> Lên
    moves = [("RIGHT", 0, 1), ("DOWN", 1, 0), ("LEFT", 0, -1), ("UP", -1, 0)]
    
    for action, dr, dc in moves:
        nr, nc = rx + dr, ry + dc
        if 0 <= nr < 4 and 0 <= nc < 4:  # Ma trận 4x4
            new_grid = list(list(row) for row in grid)
            new_grid[nr][nc] = 0  # Robot đi qua là sạch bụi
            new_grid_tuple = tuple(tuple(row) for row in new_grid)
            new_state = (nr, nc, new_grid_tuple)
            children.append(Node(new_state, node, action, node.depth + 1))
    return children

def backtrack(node):
    path = []
    while node:
        path.append(node)
        node = node.parent
    path.reverse()
    
    frames = []
    for n in path:
        rx, ry, grid = n.state
        matrix_str = []
        for r in range(4):
            row_str = []
            for c in range(4):
                if r == rx and c == ry:
                    row_str.append("'x'")
                else:
                    row_str.append(f"'{grid[r][c]}'")
            matrix_str.append("[" + " ".join(row_str) + "]")
        
        action_str = n.action if n.action else "START"
        log_msg = f"Máy đang di chuyển {action_str} đến vị trí [{rx}, {ry}]" if action_str != "START" else f"Máy đang ở vị trí xuất phát [{rx}, {ry}]"
        
        frames.append({
            "action": action_str,
            "robot_pos": (rx, ry),
            "dirt_grid": grid,
            "log_message": log_msg,
            "console_matrix": f"Hướng: {action_str}\n[" + "\n ".join(matrix_str) + "]\n"
        })
    return frames

def run_ids1(start_state, max_depth=50):
    for limit in range(max_depth):
        start_node = Node(start_state, None, None, 0)
        frontier = [start_node]
        reached = set()
        
        while frontier:
            node = frontier.pop()
            
            # Late Test: Pop ra mới kiểm tra Goal
            if is_goal(node.state):
                return backtrack(node)
                
            if node.state not in reached:
                reached.add(node.state)
                if node.depth < limit:
                    for child in reversed(get_children(node)):
                        frontier.append(child)
    return []

import time

def solve(initial_dirts):
    start_t = time.time()
    grid = []
    for r in range(4):
        row = []
        for c in range(4):
            if (r, c) in initial_dirts:
                row.append(1)
            else:
                row.append(0)
        grid.append(tuple(row))
    start_state = (0, 0, tuple(grid))
    
    frames_raw = run_ids1(start_state)
    exec_time = time.time() - start_t
    
    if not frames_raw:
        return None, "N/A", exec_time
        
    class FakeNode:
        def __init__(self, state, action, parent):
            self.state = state
            self.action = action
            self.parent = parent
            
    parent = None
    for fr in frames_raw:
        dirts = set()
        g = fr["dirt_grid"]
        for r in range(4):
            for c in range(4):
                if g[r][c] == 1:
                    dirts.add((r, c))
        
        action_map = {"RIGHT": "R", "DOWN": "D", "LEFT": "L", "UP": "U", "START": None}
        act = fr.get("action")
        action = action_map.get(act, act)
        if action == "START": action = None
        
        state = (fr["robot_pos"], frozenset(dirts))
        node = FakeNode(state, action, parent)
        parent = node
        
    return parent, "N/A", exec_time