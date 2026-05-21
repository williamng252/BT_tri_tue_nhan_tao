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
    reached_states = {root.state}
    reached_names = [root.name]
    
    node_count = 0
    
    print("=== DFS 2 (Early Test / Early Reached) ===")
    if len(root.state[1]) == 0:
        print(f"Goal reached at root node {root.name}!")
        exec_time = time.time() - start_time
        return root, node_count, exec_time
        
    while frontier:
        node = frontier.pop() # LIFO
        
        goal_node = None
        children = []
        for action, (dr, dc) in [("R", (0, 1)), ("D", (1, 0)), ("L", (0, -1)), ("U", (-1, 0))]:
            nr, nc = node.state[0][0] + dr, node.state[0][1] + dc
            if 0 <= nr < 4 and 0 <= nc < 4:
                new_dirts = node.state[1] - frozenset([(nr, nc)])
                new_state = ((nr, nc), new_dirts)
                
                if new_state not in reached_states:
                    node_count += 1
                    child = Node(new_state, parent=node, action=action, path_cost=node.path_cost + 1, name=generate_name(node_count))
                    
                    reached_states.add(child.state)
                    reached_names.append(child.name)
                    children.append(child)
                    
                    if len(child.state[1]) == 0:
                        goal_node = child
                        break
                        
        for child in reversed(children):
            frontier.append(child)
            
        if frontier:
            frontier_str = " " + ", ".join(str(n) for n in frontier) + " "
        else:
            frontier_str = ""
        reached_str = ", ".join(reached_names)
        print(f"[Pop Node: {node.name}] | Frontier: [{frontier_str}] | Reached: [{reached_str}]")
        
        if goal_node:
            print(f"Goal reached at node {goal_node.name}!")
            exec_time = time.time() - start_time
            return goal_node, node_count, exec_time
            
    print("No solution found!")
    exec_time = time.time() - start_time
    return None, node_count, exec_time

if __name__ == "__main__":
    solve({(1, 2), (2, 0), (3, 1), (3, 3)})
