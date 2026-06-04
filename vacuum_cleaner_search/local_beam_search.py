# local_beam_vacuum.py - Thuật toán Local Beam Search (Tìm kiếm chùm cục bộ)
import random
from ids1 import Node, is_goal, get_children, backtrack

class LocalBeamSearcher:
    def __init__(self, k_beams=3):
        self.k_beams = k_beams # Giới hạn chùm K (Mặc định giữ 3 trạng thái tốt nhất)

    def count_dirts(self, state):
        """Hàm Heuristic (h): Đếm số bụi"""
        grid = state[2]
        return sum(sum(row) for row in grid)

    def run_local_beam(self, start_state):
        """Chạy thuật toán Local Beam Search"""
        # 1. Khởi tạo: Sinh ngẫu nhiên k trạng thái từ Start
        current_state_set = [Node(start_state, None, None, 0)]
        for _ in range(self.k_beams - 1):
            # Tạo các biến thể ngẫu nhiên bằng cách cho Robot đi ngẫu nhiên 1-3 bước từ vạch xuất phát
            random_node = Node(start_state, None, None, 0)
            for _ in range(random.randint(1, 3)):
                children = get_children(random_node)
                if children:
                    random_node = random.choice(children)
            current_state_set.append(random_node)

        # 2. TRONG KHI (đúng):
        while True:
            neighbor_states = []
            
            # 2.1 Sinh trạng thái lân cận cho TẤT CẢ các Node trong chùm hiện tại
            for state_node in current_state_set:
                neighbor_states.extend(get_children(state_node))

            if not neighbor_states:
                print("Local Beam Search: Không còn lân cận để xét (Bế tắc)!")
                return []

            # 2.2 Kiểm tra đích
            for neighbor in neighbor_states:
                if is_goal(neighbor.state):
                    return backtrack(neighbor)

            # 2.3 Lựa chọn chùm (Nếu chưa tìm thấy đích)
            # Sắp xếp Neighbor_States theo thứ tự giá trị hàm mục tiêu h tốt dần (ít bụi nhất)
            neighbor_states.sort(key=lambda node: self.count_dirts(node.state))

            # Lọc bớt các trạng thái bị trùng lặp (do các node ở các nhánh khác nhau có thể vô tình đi tới cùng 1 ô)
            unique_neighbors = []
            seen_states = set()
            for node in neighbor_states:
                if node.state not in seen_states:
                    seen_states.add(node.state)
                    unique_neighbors.append(node)

            # Current_State_set = Lấy k trạng thái tốt nhất từ Neighbor_States đã sắp xếp
            current_state_set = unique_neighbors[:self.k_beams]
            
            # (Tùy chọn) Thêm logic chống lặp vô hạn ở đây nếu cần thiết trong tương lai

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
    
    searcher = LocalBeamSearcher()
    frames_raw = searcher.run_local_beam(start_state)
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