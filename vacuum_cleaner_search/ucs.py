# ucs_heuristic.py - Thuật toán Heuristic (Greedy Best-First) cho ma trận 4x4
import heapq
from ids1 import Node, is_goal, get_children, backtrack

def count_dirts(state):
    """Hàm Heuristic tính toán chi phí: Đếm số lượng cục bụi còn lại trên lưới"""
    grid = state[2]
    return sum(sum(row) for row in grid)

def run_ucs_heuristic(start_state):
    start_node = Node(start_state, None, None, 0)
    
    # Hàng đợi ưu tiên lưu Tuple: (chi_phi_heuristic, do_sau, id_he_thong, node_object)
    # id(child) giúp cấu trúc heap không bị lỗi so sánh khi chi phí bằng nhau
    frontier = []
    heapq.heappush(frontier, (count_dirts(start_state), 0, id(start_node), start_node))
    reached = set()
    
    while frontier:
        # Luôn tự động POP node có chi phí (số bụi còn lại) thấp nhất
        current_cost, _, _, node = heapq.heappop(frontier)
        
        if is_goal(node.state):
            return backtrack(node)
            
        if node.state not in reached:
            reached.add(node.state)
            for child in get_children(node):
                if child.state not in reached:
                    child_cost = count_dirts(child.state)
                    heapq.heappush(frontier, (child_cost, child.depth, id(child), child))
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
    
    frames_raw = run_ucs_heuristic(start_state)
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