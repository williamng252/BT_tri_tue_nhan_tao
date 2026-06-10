# belief_state_vacuum.py
from collections import deque
import heapq
import time

# =======================================================================
# HÀM CƠ BẢN DÙNG CHUNG
# =======================================================================
def is_vacuum_goal(state):
    """Kiểm tra xem mảng đã sạch bóng rác chưa (Goal)"""
    r, c, grid = state
    return sum(sum(row) for row in grid) == 0

def apply_vacuum_action(state, action):
    """Giả lập bước đi của Robot. Nếu đụng tường -> Trả về y nguyên trạng thái cũ"""
    r, c, grid = state
    new_r, new_c = r, c
    
    if action == 'U' and r > 0: new_r -= 1
    elif action == 'D' and r < 3: new_r += 1
    elif action == 'L' and c > 0: new_c -= 1
    elif action == 'R' and c < 3: new_c += 1
    else:
        return state # LUẬT ĐỤNG TƯỜNG: Đứng im, không thay đổi
        
    # Nếu đi hợp lệ, tiến hành hút rác tại ô mới
    new_grid = [list(row) for row in grid]
    if new_grid[new_r][new_c] == 1:
        new_grid[new_r][new_c] = 0
        
    return (new_r, new_c, tuple(tuple(row) for row in new_grid))

def make_grid(initial_dirts):
    grid = []
    for r in range(4):
        row = []
        for c in range(4):
            if (r, c) in initial_dirts:
                row.append(1)
            else:
                row.append(0)
        grid.append(tuple(row))
    return tuple(grid)


# =======================================================================
# LỚP ĐẠI DIỆN NODE VÀ SOLVER GIẢ LẬP FAKENODE CHO GUI
# =======================================================================
class FakeNode:
    def __init__(self, state, action, parent):
        self.state = state
        self.action = action
        self.parent = parent

def backtrack_to_fake_nodes_multi(goal_node):
    path = []
    curr = goal_node
    while curr is not None:
        path.append(curr)
        curr = curr.parent
    path.reverse()
    
    parent = None
    for node in path:
        # Lấy danh sách các vị trí của robot
        robot_positions = frozenset((s[0], s[1]) for s in node.states)
        
        # Lấy hợp tất cả bụi còn lại trên các lưới
        dirts = set()
        for s in node.states:
            grid = s[2]
            for r in range(4):
                for c in range(4):
                    if grid[r][c] == 1:
                        dirts.add((r, c))
                        
        state = (robot_positions, frozenset(dirts))
        parent = FakeNode(state, node.action, parent)
    return parent

def backtrack_to_fake_nodes_belief(goal_node):
    path = []
    curr = goal_node
    while curr is not None:
        path.append(curr)
        curr = curr.parent
    path.reverse()
    
    parent = None
    for node in path:
        # Lấy danh sách các vị trí khả thi của robot
        robot_positions = frozenset((s[0], s[1]) for s in node.belief_set)
        
        # Lấy hợp các vị trí bụi còn lại của các trạng thái trong belief
        dirts = set()
        for s in node.belief_set:
            grid = s[2]
            for r in range(4):
                for c in range(4):
                    if grid[r][c] == 1:
                        dirts.add((r, c))
                        
        state = (robot_positions, frozenset(dirts))
        parent = FakeNode(state, node.action, parent)
    return parent


# =======================================================================
# BÀI 1: TÌM KIẾM ĐA TRẠNG THÁI (MULTI-STATE SEARCH)
# =======================================================================
class MultiStateNode:
    def __init__(self, state_tuple, parent, action, g=0):
        self.states = state_tuple # Chứa tuple (Mảng 1, Mảng 2)
        self.parent = parent
        self.action = action
        self.g = g

class ParallelMultiStateSolver:
    def solve(self, start_state_1, start_state_2):
        start_node = MultiStateNode((start_state_1, start_state_2), None, None, 0)
        queue = deque([start_node])
        visited = set()
        visited.add((start_state_1, start_state_2))
        
        actions = ['L', 'R', 'U', 'D']
        node_count = 0
        
        while queue:
            current = queue.popleft()
            s1, s2 = current.states
            
            # ĐIỀU KIỆN THẮNG: Cả 2 mảng đều là Goal
            if is_vacuum_goal(s1) and is_vacuum_goal(s2):
                return current, node_count
                
            for action in actions:
                node_count += 1
                # LUẬT ĐÓNG BĂNG: Nếu mảng nào đã là Goal thì không bị tác động nữa
                if is_vacuum_goal(s1):
                    next_s1 = s1
                else:
                    next_s1 = apply_vacuum_action(s1, action)
                    
                if is_vacuum_goal(s2):
                    next_s2 = s2
                else:
                    next_s2 = apply_vacuum_action(s2, action)
                    
                next_states = (next_s1, next_s2)
                
                # Tránh lặp lại trạng thái cũ
                if next_states not in visited:
                    visited.add(next_states)
                    queue.append(MultiStateNode(next_states, current, action, current.g + 1))
                    
        return None, node_count

def run_multi_astar(start_state_1, start_state_2):
    start_node = MultiStateNode((start_state_1, start_state_2), None, None, 0)
    
    def get_h(states):
        # Heuristic: số bụi lớn nhất giữa các trạng thái
        return max(sum(sum(row) for row in s[2]) for s in states)
        
    f_start = start_node.g + get_h(start_node.states)
    
    frontier = []
    heapq.heappush(frontier, (f_start, id(start_node), start_node))
    reached = {(start_state_1, start_state_2): 0}
    
    actions = ['L', 'R', 'U', 'D']
    node_count = 0
    
    while frontier:
        _, _, current = heapq.heappop(frontier)
        s1, s2 = current.states
        
        if is_vacuum_goal(s1) and is_vacuum_goal(s2):
            return current, node_count
            
        for action in actions:
            node_count += 1
            if is_vacuum_goal(s1):
                next_s1 = s1
            else:
                next_s1 = apply_vacuum_action(s1, action)
                
            if is_vacuum_goal(s2):
                next_s2 = s2
            else:
                next_s2 = apply_vacuum_action(s2, action)
                
            next_states = (next_s1, next_s2)
            g_child = current.g + 1
            
            if next_states not in reached or g_child < reached[next_states]:
                reached[next_states] = g_child
                child = MultiStateNode(next_states, current, action, g_child)
                f_child = g_child + get_h(next_states)
                heapq.heappush(frontier, (f_child, id(child), child))
                
    return None, node_count


# =======================================================================
# BÀI 2: TÌM KIẾM TRẠNG THÁI NIỀM TIN (BELIEF STATE SEARCH)
# =======================================================================
class BeliefStateNode:
    def __init__(self, belief_set, parent, action, g=0):
        self.belief_set = belief_set 
        self.parent = parent
        self.action = action
        self.g = g

class BeliefStateSolver:
    def solve(self, list_of_possible_starts):
        start_belief = frozenset(list_of_possible_starts)
        start_node = BeliefStateNode(start_belief, None, None, 0)
        
        queue = deque([start_node])
        visited = set([start_belief])
        actions = ['L', 'R', 'U', 'D']
        node_count = 0
        
        while queue:
            current = queue.popleft()
            
            if all(is_vacuum_goal(s) for s in current.belief_set):
                return current, node_count
                
            for action in actions:
                node_count += 1
                next_belief = frozenset(apply_vacuum_action(s, action) for s in current.belief_set)
                
                if next_belief not in visited:
                    visited.add(next_belief)
                    queue.append(BeliefStateNode(next_belief, current, action, current.g + 1))
                    
        return None, node_count

def run_belief_astar(list_of_possible_starts):
    start_belief = frozenset(list_of_possible_starts)
    start_node = BeliefStateNode(start_belief, None, None, 0)
    
    def get_h(belief_set):
        if not belief_set:
            return 0
        return max(sum(sum(row) for row in s[2]) for s in belief_set)
        
    f_start = start_node.g + get_h(start_node.belief_set)
    
    frontier = []
    heapq.heappush(frontier, (f_start, id(start_node), start_node))
    reached = {start_belief: 0}
    
    actions = ['L', 'R', 'U', 'D']
    node_count = 0
    
    while frontier:
        _, _, current = heapq.heappop(frontier)
        
        if all(is_vacuum_goal(s) for s in current.belief_set):
            return current, node_count
            
        for action in actions:
            node_count += 1
            next_belief = frozenset(apply_vacuum_action(s, action) for s in current.belief_set)
            g_child = current.g + 1
            
            if next_belief not in reached or g_child < reached[next_belief]:
                reached[next_belief] = g_child
                child = BeliefStateNode(next_belief, current, action, g_child)
                f_child = g_child + get_h(next_belief)
                heapq.heappush(frontier, (f_child, id(child), child))
                
    return None, node_count


# =======================================================================
# HÀM HOẠT ĐỘNG CHO GUI
# =======================================================================
def solve_multi_bfs(initial_dirts):
    start_time = time.time()
    grid = make_grid(initial_dirts)
    start_state_1 = (0, 0, grid)
    start_state_2 = (3, 3, grid)
    
    solver = ParallelMultiStateSolver()
    goal_node, node_count = solver.solve(start_state_1, start_state_2)
    exec_time = time.time() - start_time
    
    if not goal_node:
        return None, node_count, exec_time
        
    return backtrack_to_fake_nodes_multi(goal_node), node_count, exec_time

def solve_multi_astar(initial_dirts):
    start_time = time.time()
    grid = make_grid(initial_dirts)
    start_state_1 = (0, 0, grid)
    start_state_2 = (3, 3, grid)
    
    goal_node, node_count = run_multi_astar(start_state_1, start_state_2)
    exec_time = time.time() - start_time
    
    if not goal_node:
        return None, node_count, exec_time
        
    return backtrack_to_fake_nodes_multi(goal_node), node_count, exec_time

def solve_belief_bfs(initial_dirts):
    start_time = time.time()
    grid = make_grid(initial_dirts)
    # Robot có thể bắt đầu ở bất kỳ ô nào trong 16 ô
    list_of_possible_starts = [(r, c, grid) for r in range(4) for c in range(4)]
    
    solver = BeliefStateSolver()
    goal_node, node_count = solver.solve(list_of_possible_starts)
    exec_time = time.time() - start_time
    
    if not goal_node:
        return None, node_count, exec_time
        
    return backtrack_to_fake_nodes_belief(goal_node), node_count, exec_time

def solve_belief_astar(initial_dirts):
    start_time = time.time()
    grid = make_grid(initial_dirts)
    list_of_possible_starts = [(r, c, grid) for r in range(4) for c in range(4)]
    
    goal_node, node_count = run_belief_astar(list_of_possible_starts)
    exec_time = time.time() - start_time
    
    if not goal_node:
        return None, node_count, exec_time
        
    return backtrack_to_fake_nodes_belief(goal_node), node_count, exec_time
