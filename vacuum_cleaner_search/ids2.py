# ids2.py - Thuật toán Tìm kiếm sâu dần (IDS) - Tiếp cận 2 (Early Test)
from ids1 import Node, is_goal, get_children, backtrack

def run_ids2(start_state, max_depth=50):
    # Kiểm tra Goal ngay từ trạng thái gốc
    if is_goal(start_state):
        return backtrack(Node(start_state, None, None, 0))
        
    for limit in range(1, max_depth):
        start_node = Node(start_state, None, None, 0)
        frontier = [start_node]
        reached = {start_state}
        
        while frontier:
            node = frontier.pop()
            
            if node.depth < limit:
                for child in reversed(get_children(node)):
                    if child.state not in reached:
                        # Early Test: Kiểm tra Goal ngay khi vừa sinh con
                        if is_goal(child.state):
                            return backtrack(child)
                        reached.add(child.state)
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
    
    frames_raw = run_ids2(start_state)
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