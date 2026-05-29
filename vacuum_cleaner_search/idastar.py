# idastar_vacuum.py - Thuật toán IDA* (Iterative Deepening A*)
from ids1 import Node, is_goal, get_children, backtrack

def count_dirts(state):
    """Hàm h(n): Đếm số lượng cục bụi còn lại trên lưới 4x4"""
    grid = state[2]
    return sum(sum(row) for row in grid)

def run_ida_star(start_state):
    start_node = Node(start_state, None, None, 0)
    
    # Khởi tạo Limit ban đầu I = f(Start)
    h_start = count_dirts(start_state)
    g_start = 0
    limit = g_start + h_start 
    
    while True:
        # Sử dụng Stack để chạy giống DFS
        stack = [start_node]
        
        # Cuốn sổ tay ghi lại các giá trị f bị Cutoff nhỏ nhất để nới Limit
        next_limit = float('inf') 
        
        # Dùng dictionary lưu {trạng_thái: g(n)} trên ĐƯỜNG ĐI HIỆN TẠI để tránh lặp vòng
        path_reached = {start_state: 0}
        
        goal_node = None
        
        while stack:
            node = stack.pop()
            
            if is_goal(node.state):
                goal_node = node
                break
                
            # Đẻ con và xét duyệt
            # Dùng reversed() để đảm bảo thứ tự ưu tiên của Stack (Vào cuối -> Ra đầu)
            for child in reversed(get_children(node)):
                g_child = child.depth
                h_child = count_dirts(child.state)
                f_child = g_child + h_child
                
                # NẾU VƯỢT NGƯỠNG: Bị chặn (Cutoff) và ghi vào sổ nợ
                if f_child > limit:
                    next_limit = min(next_limit, f_child)
                
                # NẾU HỢP LỆ (f <= Limit) và chưa đi qua trên đường đi này
                elif child.state not in path_reached or g_child < path_reached[child.state]:
                    path_reached[child.state] = g_child
                    stack.append(child)
                    
        # Nếu tìm thấy đích, trả về đường đi
        if goal_node:
            return backtrack(goal_node)
            
        # Nếu Stack trống rỗng mà chưa thấy Đích (Không đủ xét)
        # Nâng Limit lên bằng giá trị lố nhỏ nhất vừa ghi sổ
        if next_limit == float('inf'):
            return [] # Bế tắc hoàn toàn, không có đường đi
            
        limit = next_limit # Cập nhật I mới và vòng lặp while True sẽ tự động chạy lại từ đầu

def solve(initial_dirts):
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
    
    frames_raw = run_ida_star(start_state)
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