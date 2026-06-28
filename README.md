# Introduction to Artificial Intelligence (AI) - Project & Algorithms Visualizer

## Thông tin sinh viên
* **Họ và tên:** Nguyễn Anh Quân
* **Mã số sinh viên (MSSV):** 24110309
* **Môn học:** Introduction to Artificial Intelligence (AI) - Project & Algorithms Visualizer

📌 **Tổng quan dự án**
Dự án này là nơi lưu trữ các bài tập thực hành và đồ án nhỏ cho môn học Nhập môn Trí tuệ Nhân tạo (Introduction to AI). Nội dung bao gồm việc xây dựng các Agent phản xạ (Reflex Agents) và triển khai các thuật toán tìm kiếm từ cơ bản đến nâng cao.

Đặc biệt, dự án tích hợp một ứng dụng Trực quan hóa Thuật toán Tìm kiếm (Search Algorithms Visualizer) viết bằng giao diện đồ họa Tkinter (Python), giúp minh họa sinh động cách các thuật toán duyệt qua các không gian trạng thái, khám phá đường đi và giải quyết các bài toán kinh điển như Robot hút bụi, Tô màu bản đồ (CSP), và Cờ caro (Tic-Tac-Toe - Đối kháng).

📂 **Cấu trúc thư mục dự án**
```
AI/
├── Simple Reflex Agent/           # Các mô hình Agent phản xạ đơn giản
│   ├── 8puzzle.ipynb             # Giải bài toán 8-Puzzle bằng Simple Reflex Agent
│   ├── hutbui.ipynb              # Robot hút bụi trong môi trường đơn giản
│   └── hutbuicovatcan.ipynb      # Robot hút bụi trong môi trường có vật cản
│
├── Model Based Reflex Agent/      # Các mô hình Agent phản xạ dựa trên mô hình (Bộ nhớ/Trạng thái trong)
│   ├── 8puzzle.ipynb             # Giải 8-Puzzle sử dụng Model-Based Agent
│   └── hutbui.ipynb              # Robot hút bụi sử dụng Model-Based Agent
│
├── Algorithm/                     # Thư mục chứa các thuật toán tìm kiếm và ứng dụng trực quan
│   ├── Node.py                   # Lớp biểu diễn nút (Node) trong cây/đồ thị tìm kiếm
│   ├── Visualizer/               # Ứng dụng GUI trực quan hóa thuật toán
│   │   ├── app.py                # File chạy chính của chương trình GUI (Tkinter)
│   │   ├── visualizer.ipynb      # File Notebook thử nghiệm trực quan hóa
│   │   ├── visualizer_test.py    # Các test case kiểm thử giao diện & thuật toán
│   │   └── vacuum.png            # Asset hình ảnh của robot hút bụi
│   │
│   # Các thư mục thuật toán lõi (BFS, DFS, UCS, A*, Local Search, CSP, Adversarial...)
│   ├── BFS/
│   ├── DFS/
│   ├── UCS/
│   ├── IDS/                      # Iterative Deepening Search
│   ├── A_star/
│   ├── IDA_Star/                 # Iterative Deepening A*
│   ├── Greedy/
│   ├── Local Search/             # Hill Climbing, Simulated Annealing, Beam Search...
│   ├── CSP/                      # Constraint Satisfaction Problems (Tô màu bản đồ)
│   ├── Adversarial/              # Minimax, Alpha-Beta Pruning, Expectimax (Tic-Tac-Toe)
│   └── Search In Complex Environtment/ # Tìm kiếm trong môi trường phức tạp (Mù/Bán quan sát)
│
└── README.md                      # Tài liệu giới thiệu dự án (File này)
```

🤖 **Các thuật toán & Agent đã cài đặt**

### 1. Agents phản xạ (Reflex Agents)
* **Simple Reflex Agent:** Đưa ra quyết định hành động chỉ dựa trên cảm nhận hiện tại (Condition-Action Rules). Áp dụng cho robot hút bụi di chuyển ngẫu nhiên/theo quy tắc và giải bài toán 8-Puzzle.
* **Model-Based Reflex Agent:** Duy trì một trạng thái bên trong (Internal State / Memory) để ghi nhớ những vùng không gian đã đi qua hoặc trạng thái thế giới đã thay đổi, giúp đưa ra quyết định tối ưu hơn khi môi trường không được quan sát toàn phần.

---

🤖 **Các thuật toán tìm kiếm (6 Nhóm)**

### Nhóm 1: Uninformed Search (Tìm kiếm không thông tin / Tìm kiếm mù)
Các thuật toán tìm kiếm mù duyệt qua không gian trạng thái mà không có thông tin bổ sung về khoảng cách đến mục tiêu ngoài định nghĩa bài toán.

#### 1. BFS (Breadth-First Search)
* **Mã giả (Pseudo-code):**
  ```python
  def BFS(problem):
      node = Node(state=problem.initial_state)
      if problem.is_goal(node.state): return node
      frontier = Queue([node]) # Hàng đợi FIFO
      explored = Set()
      while not frontier.is_empty():
          node = frontier.pop()
          explored.add(node.state)
          for action in problem.actions(node.state):
              child = child_node(problem, node, action)
              if child.state not in explored and child.state not in frontier:
                  if problem.is_goal(child.state): return child
                  frontier.push(child)
      return None
  ```
* **Cách chạy cơ bản:** Lựa chọn thuật toán `BFS_1` hoặc `BFS_2` trên giao diện nhóm "Nhóm còn lại", nhấn RUN.
* **Ưu điểm:** Đầy đủ (Complete) và Tối ưu (Optimal) nếu chi phí mỗi bước đi bằng nhau.
* **Độ phức tạp thời gian:** `O(b^d)` (với `b` là hệ số nhánh, `d` là độ sâu của lời giải).
* **Độ phức tạp không gian:** `O(b^d)` (lưu toàn bộ các nút trong hàng đợi/bộ nhớ).

#### 2. DFS (Depth-First Search)
* **Mã giả (Pseudo-code):**
  ```python
  def DFS(problem):
      frontier = Stack([Node(state=problem.initial_state)]) # Ngăn xếp LIFO
      explored = Set()
      while not frontier.is_empty():
          node = frontier.pop()
          if problem.is_goal(node.state): return node
          if node.state not in explored:
              explored.add(node.state)
              for action in problem.actions(node.state):
                  frontier.push(child_node(problem, node, action))
      return None
  ```
* **Cách chạy cơ bản:** Lựa chọn `DFS_1` hoặc `DFS_2` trên giao diện nhóm "Nhóm còn lại", nhấn RUN.
* **Ưu điểm:** Tiết kiệm không gian bộ nhớ hơn BFS rất nhiều nếu cây tìm kiếm sâu nhưng hẹp.
* **Độ phức tạp thời gian:** `O(b^m)` (với `m` là độ sâu lớn nhất của cây).
* **Độ phức tạp không gian:** `O(b * m)` (chỉ lưu đường đi hiện tại và các nút chưa mở rộng cùng cấp).

#### 3. UCS (Uniform Cost Search)
* **Mã giả (Pseudo-code):**
  ```python
  def UCS(problem):
      node = Node(state=problem.initial_state)
      frontier = PriorityQueue(node, key=lambda n: n.path_cost) # Hàng đợi ưu tiên theo g(n)
      explored = Set()
      while not frontier.is_empty():
          node = frontier.pop() # Lấy nút có chi phí g(n) nhỏ nhất
          if problem.is_goal(node.state): return node
          explored.add(node.state)
          for action in problem.actions(node.state):
              child = child_node(problem, node, action)
              if child.state not in explored and child.state not in frontier:
                  frontier.push(child)
              elif child.state in frontier với chi phí cao hơn:
                  thay thế nút đó trong frontier bằng child
      return None
  ```
* **Cách chạy cơ bản:** Lựa chọn `UCS` trên giao diện nhóm "Nhóm còn lại", nhấn RUN.
* **Ưu điểm:** Đầy đủ và luôn tìm ra đường đi tối ưu với chi phí tích lũy nhỏ nhất ngay cả khi các bước có trọng số khác nhau.
* **Độ phức tạp thời gian:** `O(b^(1 + floor(C* / epsilon)))` (với `C*` là chi phí tối ưu, `epsilon` là chi phí bước tối thiểu).
* **Độ phức tạp không gian:** `O(b^(1 + floor(C* / epsilon)))` (lưu tất cả các nút đã duyệt).

#### 4. IDS (Iterative Deepening Search)
* **Mã giả (Pseudo-code):**
  ```python
  def IDS(problem):
      for depth in range(0, infinity):
          result = Depth_Limited_Search(problem, depth)
          if result != cutoff: return result
  ```
* **Cách chạy cơ bản:** Lựa chọn `IDS_1` hoặc `IDS_2` trên giao diện nhóm "Nhóm còn lại", nhấn RUN.
* **Ưu điểm:** Kết hợp tính tối ưu, đầy đủ của BFS và tính tiết kiệm bộ nhớ của DFS.
* **Độ phức tạp thời gian:** `O(b^d)`
* **Độ phức tạp không gian:** `O(b * d)`

---

### Nhóm 2: Informed Search (Tìm kiếm có thông tin / Heuristic)
Sử dụng hàm ước lượng `h(n)` để định hướng tìm kiếm thông minh hơn về phía mục tiêu.

#### 1. Greedy Best-First Search
* **Mã giả (Pseudo-code):**
  ```python
  def Greedy_Best_First(problem):
      node = Node(state=problem.initial_state)
      frontier = PriorityQueue(node, key=lambda n: heuristic(n.state)) # Theo h(n)
      explored = Set()
      while not frontier.is_empty():
          node = frontier.pop()
          if problem.is_goal(node.state): return node
          explored.add(node.state)
          for action in problem.actions(node.state):
              child = child_node(problem, node, action)
              if child.state not in explored and child.state not in frontier:
                  frontier.push(child)
      return None
  ```
* **Cách chạy cơ bản:** Chọn `Greedy` từ danh sách thuật toán nhóm "Nhóm còn lại", nhấn RUN.
* **Ưu điểm:** Tốc độ tìm kiếm rất nhanh nếu có một hàm heuristic tốt và chính xác.
* **Độ phức tạp thời gian:** `O(b^m)` (trường hợp tệ nhất), nhưng thực tế thường rất nhanh.
* **Độ phức tạp không gian:** `O(b^m)` (lưu trữ tất cả các nút trong hàng đợi).

#### 2. A* Search
* **Mã giả (Pseudo-code):**
  ```python
  def A_Star(problem):
      node = Node(state=problem.initial_state)
      # Sắp xếp theo f(n) = g(n) + h(n)
      frontier = PriorityQueue(node, key=lambda n: n.path_cost + heuristic(n.state))
      explored = Set()
      while not frontier.is_empty():
          node = frontier.pop()
          if problem.is_goal(node.state): return node
          explored.add(node.state)
          for action in problem.actions(node.state):
              child = child_node(problem, node, action)
              if child.state not in explored and child.state not in frontier:
                  frontier.push(child)
              elif child.state in frontier với f(n) lớn hơn:
                  thay thế nút đó trong frontier bằng child
      return None
  ```
* **Cách chạy cơ bản:** Chọn `A_star` trên giao diện nhóm "Nhóm còn lại", nhấn RUN.
* **Ưu điểm:** Đầy đủ và tối ưu nhất (nếu heuristic là chấp nhận được - admissible và nhất quán - consistent).
* **Độ phức tạp thời gian:** Số nút được duyệt tăng theo hàm mũ `O(b^d)` phụ thuộc vào độ dài lời giải.
* **Độ phức tạp không gian:** `O(b^d)` (giữ toàn bộ các nút trong bộ nhớ).

#### 3. IDA* (Iterative Deepening A*)
* **Mã giả (Pseudo-code):**
  ```python
  def IDA_Star(problem):
      limit = heuristic(problem.initial_state)
      while True:
          temp_limit, result = DLS_A_Star(problem.initial_state, 0, limit)
          if result == goal: return result
          if temp_limit == infinity: return None
          limit = temp_limit
  ```
* **Cách chạy cơ bản:** Chọn `Ids_A_atar` trên giao diện nhóm "Nhóm còn lại", nhấn RUN.
* **Ưu điểm:** Tiết kiệm bộ nhớ hơn A* thông thường bằng cách áp dụng phương pháp sâu dần dựa trên giới hạn chi phí `f(n)`.
* **Độ phức tạp thời gian:** `O(b^d)`
* **Độ phức tạp không gian:** `O(b * d)`

---

### Nhóm 3: Local Search (Tìm kiếm cục bộ)
Tập trung vào tối ưu hóa trạng thái hiện tại thay vì tìm đường đi từ đầu.

#### 1. Hill Climbing (Leo đồi) & Các biến thể (Simple, Steepest-Ascent, Stochastic, Random Restart)
* **Mã giả (Steepest-Ascent):**
  ```python
  def Hill_Climbing(problem):
      current = problem.initial_state
      while True:
          neighbors = problem.neighbors(current)
          best_neighbor = max(neighbors, key=lambda n: value(n))
          if value(best_neighbor) <= value(current):
              return current
          current = best_neighbor
  ```
* **Cách chạy cơ bản:** Chọn lần lượt `Simple_Hill`, `Steepest Ascent`, `Stochastic` hoặc `Random Restart` trên giao diện nhóm "Nhóm còn lại", nhấn RUN.
* **Ưu điểm:** Cực kỳ tiết kiệm bộ nhớ (chỉ lưu trạng thái hiện tại), thích hợp cho không gian trạng thái vô hạn hoặc cực lớn.
* **Độ phức tạp thời gian:** Phụ thuộc vào cấu trúc của không gian trạng thái; dễ mắc kẹt ở cực trị địa phương (local maxima) hoặc cao nguyên (plateaus).
* **Độ phức tạp không gian:** `O(1)` (hằng số).

#### 2. Beam Search (Tìm kiếm chùm tia)
* **Mã giả (Pseudo-code):**
  ```python
  def Beam_Search(problem, k):
      frontier = [problem.initial_state]
      while not goal_found:
          candidates = []
          for state in frontier:
              candidates.extend(problem.neighbors(state))
          frontier = select_best_k(candidates, k) # Giữ lại k trạng thái tốt nhất
          if goal in frontier: return goal
      return None
  ```
* **Cách chạy cơ bản:** Chọn `Beam Search` (chương trình mặc định cấu hình song song `k = 2`), nhấn RUN.
* **Ưu điểm:** Duyệt rộng hơn leo đồi nhờ giữ lại `k` trạng thái tốt nhất song song, giảm nguy cơ mắc kẹt.
* **Độ phức tạp thời gian:** `O(k * b * m)` (với `m` là số bước tối đa).
* **Độ phức tạp không gian:** `O(k * b)` (lưu giữ `k` trạng thái và các nút con của chúng).

#### 3. Simulated Annealing (Luyện kim giả lập)
* **Mã giả (Pseudo-code):**
  ```python
  def Simulated_Annealing(problem, schedule):
      current = problem.initial_state
      for t in range(1, infinity):
          T = schedule(t) # Nhiệt độ giảm dần
          if T == 0: return current
          next_state = random_select(problem.neighbors(current))
          delta_E = value(next_state) - value(current)
          if delta_E > 0:
              current = next_state
          else:
              # Chấp nhận trạng thái tệ hơn với xác suất e^(delta_E / T)
              current = next_state with probability e^(delta_E / T)
  ```
* **Cách chạy cơ bản:** Chọn `Simulate Annealing` trên giao diện nhóm "Nhóm còn lại", nhấn RUN.
* **Ưu điểm:** Có khả năng thoát khỏi cực trị địa phương nhờ cơ chế nhảy ngẫu nhiên chấp nhận bước đi tệ hơn dựa trên nhiệt độ giảm dần.
* **Độ phức tạp thời gian:** Phụ thuộc vào tốc độ giảm nhiệt độ (cooling schedule), nhưng có khả năng hội tụ về tối ưu toàn cục.
* **Độ phức tạp không gian:** `O(1)`.

---

### Nhóm 4: Search in Complex Environments (Tìm kiếm trong môi trường phức tạp - Bán quan sát/Không cảm biến)
Giải quyết bài toán khi môi trường không được quan sát đầy đủ bằng cách tìm kiếm trên không gian trạng thái niềm tin (Belief States).

#### 1. Sensorless Search (Tìm kiếm không cảm biến / Mù hoàn toàn)
* **Mã giả (Sử dụng BFS trên Belief States):**
  ```python
  def Sensorless_Search_BFS(problem):
      start_belief = problem.initial_belief_state
      frontier = Queue([Node(start_belief, parent=None, action=None)])
      explored = Set()
      while not frontier.is_empty():
          node = frontier.pop()
          if problem.is_goal(node.state): return node.path()
          explored.add(hash_belief(node.state))
          for action in problem.actions:
              next_belief = predict_belief(node.state, action)
              if hash_belief(next_belief) not in explored and next_belief not in frontier:
                  frontier.push(Node(next_belief, parent=node, action=action))
      return None
  ```
* **Cách chạy cơ bản:** Chọn 1. `Thuật toán tìm kiếm mù` trên menu, chọn thuật toán `Mù Start (BFS)` hoặc `Mù Goal (DFS)`, nhấn RUN.
* **Ưu điểm:** Tìm ra chuỗi hành động đảm bảo đưa hệ thống về trạng thái mục tiêu kể cả khi hoàn toàn không có cảm biến để biết vị trí/trạng thái hiện tại.
* **Độ phức tạp thời gian:** `O(b^P)` (với `P` là số trạng thái niềm tin tối đa, tối đa là `2^N` với `N` là số trạng thái vật lý của thế giới).
* **Độ phức tạp không gian:** `O(2^N)` (để lưu trữ tất cả các trạng thái niềm tin tiềm năng).

#### 2. Partial Observation Search (Tìm kiếm quan sát bộ phận)
* **Mã giả (Pseudo-code):**
  ```python
  # Dự đoán trạng thái niềm tin tiếp theo dựa trên hành động và kết quả từ cảm biến:
  # Belief_State_Next = Update(Predict(Belief_State, Action), Percept)
  # Xây dựng cây AND-OR search hoặc kết hợp để tìm kế hoạch hành động thích ứng (Contingency Plan)
  ```
* **Cách chạy cơ bản:** Chọn `Mù Partial` từ danh sách thuật toán mù, nhấn RUN.
* **Ưu điểm:** Cho phép robot cập nhật niềm tin động từ dữ liệu cảm biến hữu hạn, tìm ra phương án tối ưu hơn so với mù hoàn toàn.
* **Độ phức tạp thời gian:** Thuộc lớp độ phức tạp lũy thừa theo số trạng thái vật lý `O(2^N)` trong trường hợp xấu nhất, nhưng nhanh hơn trong thực tế nhờ các thông tin cảm biến giúp loại bỏ nhiều trạng thái phi lý.
* **Độ phức tạp không gian:** `O(2^N)`.

---

### Nhóm 5: Constraint Satisfaction Problems (CSP - Bài toán thỏa mãn ràng buộc)
Giải quyết bài toán bằng cách phân bổ các giá trị vào biến sao cho thỏa mãn các ràng buộc định trước.

#### 1. Backtracking Search (Quay lui)
* **Mã giả (Pseudo-code):**
  ```python
  def Backtracking_Search(csp):
      return Backtrack({}, csp)

  def Backtrack(assignment, csp):
      if is_complete(assignment, csp): return assignment
      var = select_unassigned_variable(assignment, csp)
      for value in order_domain_values(var, assignment, csp):
          if is_consistent(var, value, assignment, csp):
              assignment.add(var, value)
              result = Backtrack(assignment, csp)
              if result != failure: return result
              assignment.remove(var, value)
      return failure
  ```
* **Cách chạy cơ bản:** Vào menu chọn `3. Tô màu bản đồ (CSP)`, chọn thuật toán `Backtracking`, nhấn RUN.
* **Ưu điểm:** Đơn giản, đảm bảo tìm ra lời giải hợp lệ nếu tồn tại trong không gian lời giải hữu hạn.
* **Độ phức tạp thời gian:** `O(d^n)` (trong đó `d` là số lượng giá trị trong miền giá trị, `n` là số biến).
* **Độ phức tạp không gian:** `O(n)` (độ sâu đệ quy lớn nhất bằng số lượng biến).

#### 2. Forward Checking (Kiểm tra trước)
* **Mã giả (Pseudo-code):**
  ```python
  def Forward_Checking(assignment, csp, var, value):
      assignment.add(var, value)
      for neighbor in csp.neighbors(var):
          if neighbor not in assignment:
              remove value from neighbor.domain if it violates constraints
              if neighbor.domain is empty:
                  return failure
      return success
  ```
* **Cách chạy cơ bản:** Vào menu chọn `3. Tô màu bản đồ (CSP)`, chọn thuật toán `Forward Checking`, nhấn RUN.
* **Ưu điểm:** Phát hiện sớm các nhánh không có lời giải trước khi đi sâu vào đệ quy, giảm kích thước cây tìm kiếm một cách đáng kể.
* **Độ phức tạp thời gian:** Nhỏ hơn nhiều so với Backtracking thuần túy (nhỏ hơn `O(d^n)` trong thực tế).
* **Độ phức tạp không gian:** `O(n * d)` (để lưu trữ miền giá trị bị thu hẹp của các biến tại mỗi cấp đệ quy).

---

### Nhóm 6: Adversarial Search (Tìm kiếm đối kháng)
Tìm kiếm các nước đi tối ưu trong môi trường có sự đối kháng của đối thủ (trò chơi tổng bằng không).

#### 1. Minimax
* **Mã giả (Pseudo-code):**
  ```python
  def Minimax_Decision(state):
      return argmax(actions, key=lambda a: Min_Value(Result(state, a)))

  def Max_Value(state):
      if Terminal_Test(state): return Utility(state)
      v = -infinity
      for action in Actions(state):
          v = max(v, Min_Value(Result(state, action)))
      return v

  def Min_Value(state):
      if Terminal_Test(state): return Utility(state)
      v = infinity
      for action in Actions(state):
          v = min(v, Max_Value(Result(state, action)))
      return v
  ```
* **Cách chạy cơ bản:** Vào menu chọn `4. Thuật toán đối kháng`, click chọn một ô trống trên bảng Caro 3x3 để đi trước, chọn thuật toán `Minimax`, nhấn RUN để máy chơi nước đi đối kháng của nó.
* **Ưu điểm:** Lựa chọn tối ưu nhất nếu đối thủ chơi thông minh tuyệt đối theo lý thuyết trò chơi.
* **Độ phức tạp thời gian:** `O(b^m)` (với `b` là hệ số nhánh, `m` là độ sâu tối đa của trò chơi).
* **Độ phức tạp không gian:** `O(b * m)`

#### 2. Alpha-Beta Pruning (Cắt tỉa Alpha-Beta)
* **Mã giả (Pseudo-code):**
  ```python
  def Alpha_Beta_Search(state):
      v = Max_Value(state, -infinity, +infinity)
      return action_leading_to_v

  def Max_Value(state, alpha, beta):
      if Terminal_Test(state): return Utility(state)
      v = -infinity
      for action in Actions(state):
          v = max(v, Min_Value(Result(state, action), alpha, beta))
          if v >= beta: return v
          alpha = max(alpha, v)
      return v

  def Min_Value(state, alpha, beta):
      if Terminal_Test(state): return Utility(state)
      v = +infinity
      for action in Actions(state):
          v = min(v, Max_Value(Result(state, action), alpha, beta))
          if v <= alpha: return v
          beta = min(beta, v)
      return v
  ```
* **Cách chạy cơ bản:** Tương tự Minimax, chọn thuật toán `Alpha-Beta`, đặt quân cờ và nhấn RUN.
* **Ưu điểm:** Giảm đáng kể số lượng nút phải duyệt bằng cách cắt bỏ các nhánh không ảnh hưởng đến quyết định cuối cùng, kết quả nước đi tương đương Minimax.
* **Độ phức tạp thời gian:** Trường hợp tốt nhất là `O(b^(m/2))` (nhanh gấp đôi so với Minimax).
* **Độ phức tạp không gian:** `O(b * m)`.

#### 3. Expectimax
* **Mã giả (Pseudo-code):**
  ```python
  def Expectimax_Decision(state):
      return argmax(actions, key=lambda a: Expect_Value(Result(state, a)))

  def Expect_Value(state):
      if Terminal_Test(state): return Utility(state)
      v = 0
      actions = Actions(state)
      probability = 1.0 / len(actions) # Phân phối xác suất đều của đối thủ ngẫu nhiên
      for action in actions:
          v += probability * Max_Value(Result(state, action))
      return v
  ```
* **Cách chạy cơ bản:** Tương tự Minimax, chọn thuật toán `Expectimax`, đặt quân cờ và nhấn RUN.
* **Ưu điểm:** Vượt trội hơn Minimax khi đối thủ không chơi tối ưu mà đưa ra hành động ngẫu nhiên hoặc môi trường có tính may rủi.
* **Độ phức tạp thời gian:** `O(b^m)`.
* **Độ phức tạp không gian:** `O(b * m)`.
