# hill_climbing_vacuum.py - Thuật toán Local Search (Leo Đồi)
import random
from ids1 import Node, is_goal, get_children, backtrack

class HillClimbingSearcher:
    def __init__(self, max_sideways_moves=10):
        # Số bước đi ngang tối đa cho phép để tránh lặp vòng vô hạn ở Cao nguyên
        self.max_sideways_moves = max_sideways_moves
        
    def count_dirts(self, state):
        grid = state[2]
        return sum(sum(row) for row in grid)

    def run_simple(self, start_state):
        """1. Leo đồi đơn giản: Thấy tốt hơn là nhảy sang ngay lập tức"""
        current_node = Node(start_state, None, None, 0)
        
        while not is_goal(current_node.state):
            current_h = self.count_dirts(current_node.state)
            neighbors = get_children(current_node)
            
            found_better = False
            for child in neighbors:
                child_h = self.count_dirts(child.state)
                # Tốt hơn (Bụi ít hơn) -> Chốt luôn! Bỏ qua các con phía sau
                if child_h < current_h:
                    current_node = child
                    found_better = True
                    break 
            
            # Nếu xét hết con mà không có thằng nào tốt hơn -> Kẹt ở Đỉnh giả
            if not found_better:
                print("Simple Hill Climbing: Bị kẹt tại Local Minimum!")
                return backtrack(current_node)
                
        return backtrack(current_node)

    def run_steepest(self, start_state):
        """2. Leo đồi dốc nhất: Xét tất cả, chọn thằng xuất sắc nhất (Có hỗ trợ đi ngang)"""
        current_node = Node(start_state, None, None, 0)
        sideways_count = 0
        
        while not is_goal(current_node.state):
            current_h = self.count_dirts(current_node.state)
            neighbors = get_children(current_node)
            
            if not neighbors:
                break
                
            scored_neighbors = [(self.count_dirts(c.state), c) for c in neighbors]
            best_h = min(score for score, _ in scored_neighbors)
            best_children = [c for score, c in scored_neighbors if score == best_h]
            
            if best_h < current_h:
                current_node = random.choice(best_children)
                sideways_count = 0 
                
            elif best_h == current_h:
                if sideways_count < self.max_sideways_moves:
                    current_node = random.choice(best_children)
                    sideways_count += 1
                else:
                    print(f"Steepest Ascent: Đã đi ngang {self.max_sideways_moves} bước. Dừng để tránh lặp vô hạn!")
                    break
            else:
                print("Steepest Ascent: Bị kẹt tại Local Minimum!")
                break
                
        return backtrack(current_node)

    def run_stochastic(self, start_state):
        """3. Leo đồi ngẫu nhiên: Lấy tất cả thằng BẰNG hoặc TỐT HƠN, random đại 1 thằng"""
        current_node = Node(start_state, None, None, 0)
        sideways_count = 0
        
        while not is_goal(current_node.state):
            current_h = self.count_dirts(current_node.state)
            neighbors = get_children(current_node)
            
            acceptable_neighbors = []
            for child in neighbors:
                if self.count_dirts(child.state) <= current_h:
                    acceptable_neighbors.append(child)
            
            if not acceptable_neighbors:
                print("Stochastic Hill Climbing: Bị kẹt tại Local Minimum!")
                break
                
            next_node = random.choice(acceptable_neighbors)
            next_h = self.count_dirts(next_node.state)
            
            if next_h == current_h:
                sideways_count += 1
                if sideways_count > self.max_sideways_moves:
                    print("Stochastic Hill Climbing: Bị kẹt vòng lặp đi ngang!")
                    break
            else:
                sideways_count = 0 
                
            current_node = next_node
            
        return backtrack(current_node)

    def run_random_restart(self, start_state, max_restart=10):
        """4. Random Restart Hill Climbing (Leo đồi khởi tạo ngẫu nhiên)"""
        for i in range(max_restart):
            # Lần đầu tiên thử chạy với trạng thái gốc của user
            if i == 0:
                current_node = Node(start_state, None, None, 0)
            else:
                # Sinh trạng thái ngẫu nhiên (Robot rơi xuống 1 ô bất kỳ, map rác tạo ngẫu nhiên)
                r, c = random.randint(0, 3), random.randint(0, 3)
                random_grid = tuple(tuple(random.choice([0, 1]) for _ in range(4)) for _ in range(4))
                current_node = Node((r, c, random_grid), None, None, 0)

            while True:
                if is_goal(current_node.state):
                    return backtrack(current_node)

                current_h = self.count_dirts(current_node.state)
                neighbors = get_children(current_node)

                # Lọc ra tập Better_Neighbors (Tốt hơn hẳn trạng thái hiện tại)
                better_neighbors = [child for child in neighbors if self.count_dirts(child.state) < current_h]

                if not better_neighbors:
                    print(f"Lượt {i+1}: Kẹt tại Đỉnh giả cục bộ! Kích hoạt Random Restart...")
                    break  # Thoát vòng lặp WHILE, nhảy sang lượt i tiếp theo của vòng FOR
                else:
                    # Next_State = Chọn trạng thái tốt nhất từ Better_Neighbors
                    best_child = min(better_neighbors, key=lambda c: self.count_dirts(c.state))
                    current_node = best_child

        print("Random_Restart_Hill_Climbing: Thất bại! Đã chạy hết MAX_RESTART lượt.")
        return []

import time

def solve_helper(frames_raw, exec_time):
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

def solve_simple(initial_dirts):
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
    
    searcher = HillClimbingSearcher()
    frames_raw = searcher.run_simple(start_state)
    exec_time = time.time() - start_t
    return solve_helper(frames_raw, exec_time)

def solve_steepest(initial_dirts):
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
    
    searcher = HillClimbingSearcher()
    frames_raw = searcher.run_steepest(start_state)
    exec_time = time.time() - start_t
    return solve_helper(frames_raw, exec_time)

def solve_stochastic(initial_dirts):
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
    
    searcher = HillClimbingSearcher()
    frames_raw = searcher.run_stochastic(start_state)
    exec_time = time.time() - start_t
    return solve_helper(frames_raw, exec_time)

def solve_random_restart(initial_dirts):
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
    
    searcher = HillClimbingSearcher()
    frames_raw = searcher.run_random_restart(start_state)
    exec_time = time.time() - start_t
    return solve_helper(frames_raw, exec_time)