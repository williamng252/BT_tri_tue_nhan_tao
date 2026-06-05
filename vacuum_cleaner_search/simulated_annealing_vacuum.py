# simulated_annealing_vacuum.py - Thuật toán Luyện kim mô phỏng
import math
import random
from ids1 import Node, is_goal, get_children, backtrack

class SimulatedAnnealingSearcher:
    def __init__(self, T0=100.0, Tmin=0.01, alpha=0.95):
        # T0: Nhiệt độ ban đầu (Càng cao càng dễ đi lung tung lúc đầu)
        # Tmin: Nhiệt độ tối thiểu để dừng thuật toán
        # alpha: Tốc độ làm lạnh (Thường từ 0.8 đến 0.99)
        self.T0 = T0
        self.Tmin = Tmin
        self.alpha = alpha

    def count_dirts(self, state):
        """Hàm Heuristic (h): Đếm số cục bụi"""
        grid = state[2]
        return sum(sum(row) for row in grid)

    def run_simulated_annealing(self, start_state):
        # current state = start
        current_node = Node(start_state, None, None, 0)
        
        # T = T0
        T = self.T0

        # while T > Tmin:
        while T > self.Tmin:
            # if current state == goal: return current state
            if is_goal(current_node.state):
                return backtrack(current_node)

            # Sinh tất cả lân cận và lấy ngẫu nhiên 1 thằng
            # next state = RandomNeighbor(current state)
            neighbors = get_children(current_node)
            if not neighbors:
                break  # Bế tắc không có đường đi
                
            next_node = random.choice(neighbors)

            # Tính delta: Δ = h(next state) - h(current state)
            current_h = self.count_dirts(current_node.state)
            next_h = self.count_dirts(next_node.state)
            delta = next_h - current_h

            # if Δ < 0: current state = next state (Trạng thái tốt hơn -> Chọn luôn)
            if delta < 0:
                current_node = next_node
            else:
                # else: p = exp(-Δ / T)
                # Chấp nhận trạng thái TỆ HƠN với xác suất p
                p = math.exp(-delta / T)
                
                # if Random(0,1) < p: current state = next state
                if random.random() < p:
                    current_node = next_node

            # Giảm nhiệt độ: T = α * T
            T = self.alpha * T

        # return current state (Trả về đường đi tốt nhất tìm được khi đã nguội lạnh)
        return backtrack(current_node)

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
    
    searcher = SimulatedAnnealingSearcher()
    frames_raw = searcher.run_simulated_annealing(start_state)
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