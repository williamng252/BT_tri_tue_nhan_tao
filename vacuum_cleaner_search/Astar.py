# astar_vacuum.py - Thuật toán A* (A-Star)
import heapq
from ids1 import Node, is_goal, get_children, backtrack

def count_dirts(state):
    """Hàm h(n): Đếm số cục bụi còn lại"""
    grid = state[2]
    return sum(sum(row) for row in grid)

def run_astar(start_state):
    start_node = Node(start_state, None, None, 0)
    
    # Tính f(Start)
    h_start = count_dirts(start_state)
    g_start = 0 # Tại điểm xuất phát, số bước đi = 0
    f_start = g_start + h_start
    
    # Priority Queue lưu Tuple: (f(n), id_node, Node)
    frontier = []
    heapq.heappush(frontier, (f_start, id(start_node), start_node))
    
    # Dùng Dictionary lưu {trạng_thái: g(n)_nhỏ_nhất} để áp dụng đúng luật A*
    reached = {start_state: g_start}
    
    while frontier:
        # Lôi Node có f(n) = g(n) + h(n) NHỎ NHẤT ra xét
        current_f, _, node = heapq.heappop(frontier)
        
        if is_goal(node.state):
            return backtrack(node)
            
        for child in get_children(node):
            # Tính g(n), h(n) và f(n) cho con
            g_child = child.depth  # Chi phí thực tế chính là độ sâu (số bước đi)
            h_child = count_dirts(child.state)
            f_child = g_child + h_child
            
            # Cập nhật theo luật A*:
            # Nếu trạng thái m chưa có trong REACHED, HOẶC tìm được đường đi (g_child) ngắn hơn
            if child.state not in reached or g_child < reached[child.state]:
                reached[child.state] = g_child
                heapq.heappush(frontier, (f_child, id(child), child))
                
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
    
    frames_raw = run_astar(start_state)
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