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
                return backtrack(current_node) # Trả về đường đi đến chỗ bị kẹt
                
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
                
            # Tính h cho tất cả các con
            scored_neighbors = [(self.count_dirts(c.state), c) for c in neighbors]
            # Tìm điểm h nhỏ nhất (tốt nhất)
            best_h = min(score for score, _ in scored_neighbors)
            
            # Lọc ra tất cả các con đạt được điểm best_h này (có thể có nhiều con cùng điểm)
            best_children = [c for score, c in scored_neighbors if score == best_h]
            
            if best_h < current_h:
                # Tìm thấy chỗ dốc hơn -> Random 1 thằng trong đám tốt nhất và đi tiếp
                current_node = random.choice(best_children)
                sideways_count = 0 # Reset đếm đi ngang
                
            elif best_h == current_h:
                # Cao nguyên (Plateau) -> Bằng nhau lấy random chạy tiếp
                if sideways_count < self.max_sideways_moves:
                    current_node = random.choice(best_children)
                    sideways_count += 1
                else:
                    print(f"Steepest Ascent: Đã đi ngang {self.max_sideways_moves} bước. Dừng để tránh lặp vô hạn!")
                    break
            else:
                # Mọi hướng đều tệ hơn -> Kẹt Đỉnh giả
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
            
            # Lọc ra danh sách những đứa đạt yêu cầu (h <= hiện tại)
            acceptable_neighbors = []
            for child in neighbors:
                if self.count_dirts(child.state) <= current_h:
                    acceptable_neighbors.append(child)
            
            if not acceptable_neighbors:
                print("Stochastic Hill Climbing: Bị kẹt tại Local Minimum!")
                break
                
            # Random nhắm mắt bốc đại 1 con trong danh sách hợp lệ
            next_node = random.choice(acceptable_neighbors)
            next_h = self.count_dirts(next_node.state)
            
            if next_h == current_h:
                sideways_count += 1
                if sideways_count > self.max_sideways_moves:
                    print("Stochastic Hill Climbing: Bị kẹt vòng lặp đi ngang!")
                    break
            else:
                sideways_count = 0 # Đi được xuống dốc thì reset đếm ngang
                
            current_node = next_node
            
        return backtrack(current_node)

def _solve_helper(initial_dirts, run_func):
    import time
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
    frames_raw = run_func(searcher, start_state)
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

def solve_simple(initial_dirts):
    return _solve_helper(initial_dirts, lambda s, state: s.run_simple(state))

def solve_steepest(initial_dirts):
    return _solve_helper(initial_dirts, lambda s, state: s.run_steepest(state))

def solve_stochastic(initial_dirts):
    return _solve_helper(initial_dirts, lambda s, state: s.run_stochastic(state))