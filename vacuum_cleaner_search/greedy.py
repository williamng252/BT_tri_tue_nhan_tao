# greedy_vacuum.py - Greedy Best-First Search (Tìm kiếm Tham lam)
import heapq
from ids1 import Node, is_goal, get_children, backtrack

def count_dirts(state):
    """Hàm h(n): Đếm số lượng cục bụi còn lại trên lưới 4x4"""
    grid = state[2]
    return sum(sum(row) for row in grid)

def run_greedy(start_state):
    start_node = Node(start_state, None, None, 0)
    
    # Priority Queue lưu Tuple: (h(n), id_node, Node)
    frontier = []
    heapq.heappush(frontier, (count_dirts(start_state), id(start_node), start_node))
    reached = set()
    
    while frontier:
        # Lôi Node có h(n) NHỎ NHẤT (ít bụi nhất) ra xét
        current_h, _, node = heapq.heappop(frontier)
        
        # Test Goal khi POP (Late Test)
        if is_goal(node.state):
            return backtrack(node)
            
        if node.state not in reached:
            reached.add(node.state)
            
            for child in get_children(node):
                if child.state not in reached:
                    # Gán h(n) mới cho Node con và đẩy vào Hàng đợi
                    h_child = count_dirts(child.state)
                    heapq.heappush(frontier, (h_child, id(child), child))
                    
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
    
    frames_raw = run_greedy(start_state)
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