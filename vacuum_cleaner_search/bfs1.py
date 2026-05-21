import time

def generate_name(index):
    name = ""
    while index >= 0:
        name = chr(65 + (index % 26)) + name
        index = index // 26 - 1
    return name

def state_to_string(state):
    robot_pos, dirts = state
    rows = []
    for r in range(4):
        row = ""
        for c in range(4):
            if (r, c) == robot_pos:
                row += "X"
            elif (r, c) in dirts:
                row += "1"
            else:
                row += "0"
        rows.append(row)
    return "|".join(rows)

class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0, name="A"):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.name = name

    def __str__(self):
        state_str = state_to_string(self.state)
        parent_name = self.parent.name if self.parent else "None"
        action_name = self.action if self.action else "None"
        return f"{{{state_str}, {parent_name}, {action_name}, {self.path_cost}}} {self.name}"

def solve(initial_dirts):
    start_time = time.time()
    initial_state = ((0,0), frozenset(initial_dirts))
    root = Node(initial_state, name="A")
    frontier = [root]
    reached_states = set()
    reached_names = []
    
    node_count = 0
    
    print("=== BFS 1 (Late Test / Late Reached) ===")
    while frontier:
        node = frontier.pop(0) # FIFO
        
        if node.state in reached_states:
            if frontier:
                frontier_str = " " + ", ".join(str(n) for n in frontier) + " "
            else:
                frontier_str = ""
            reached_str = ", ".join(reached_names)
            print(f"[Pop Node: {node.name} (Skip/Duplicate)] | Frontier: [{frontier_str}] | Reached: [{reached_str}]")
            continue
            
        is_goal = len(node.state[1]) == 0
        
        reached_states.add(node.state)
        reached_names.append(node.name)
        
        if not is_goal:
            for action, (dr, dc) in [("R", (0, 1)), ("D", (1, 0)), ("L", (0, -1)), ("U", (-1, 0))]:
                nr, nc = node.state[0][0] + dr, node.state[0][1] + dc
                if 0 <= nr < 4 and 0 <= nc < 4:
                    new_dirts = node.state[1] - frozenset([(nr, nc)])
                    new_state = ((nr, nc), new_dirts)
                    
                    node_count += 1
                    child = Node(new_state, parent=node, action=action, path_cost=node.path_cost + 1, name=generate_name(node_count))
                    frontier.append(child)
                    
        if frontier:
            frontier_str = " " + ", ".join(str(n) for n in frontier) + " "
        else:
            frontier_str = ""
        reached_str = ", ".join(reached_names)
        print(f"[Pop Node: {node.name}] | Frontier: [{frontier_str}] | Reached: [{reached_str}]")
        
        if is_goal:
            print(f"Goal reached at node {node.name}!")
            exec_time = time.time() - start_time
            return node, node_count, exec_time
            
    print("No solution found!")
    exec_time = time.time() - start_time
    return None, node_count, exec_time

if __name__ == "__main__":
    solve({(1, 2), (2, 0), (3, 1), (3, 3)})
