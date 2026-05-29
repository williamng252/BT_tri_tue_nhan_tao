import tkinter as tk
from tkinter import scrolledtext, messagebox
import bfs1
import bfs2
import dfs1
import dfs2
import ids1
import ids2
import ucs
import greedy
import Astar
import idastar
import hill_climbing

class VacuumVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Mô Phỏng AI Máy Hút Bụi 4x4")
        self.root.geometry("1100x750")
        self.root.configure(bg="#f4f4f4")
        
        self.is_running = False
        self.group_states = {
            "bfs": False,
            "dfs": False,
            "ids": False,
            "hill": False,
            "others": False
        }
        
        self.create_widgets()
        self.reset_state()
        
    def create_widgets(self):
        # Khu vực Trái (Menu)
        left_frame = tk.Frame(self.root, width=220, bg="#ffffff", relief="ridge", borderwidth=2)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        tk.Label(left_frame, text="ĐIỀU KHIỂN", font=("Segoe UI", 14, "bold"), bg="#ffffff").pack(pady=10)
        
        btn_config = {"font": ("Segoe UI", 11), "width": 20, "cursor": "hand2"}
        btn_toggle_config = {"font": ("Segoe UI", 11, "bold"), "width": 20, "cursor": "hand2", "relief": "raised", "bd": 1}
        btn_sub_config = {"font": ("Segoe UI", 10), "width": 20, "cursor": "hand2", "relief": "groove", "bd": 1}
        
        # --- 1. Nhóm BFS ---
        self.bfs_container = tk.Frame(left_frame, bg="#ffffff")
        self.bfs_container.pack(fill=tk.X, pady=3)
        
        self.btn_bfs_toggle = tk.Button(self.bfs_container, text="🔍 BFS Search  ▸", bg="#e3f2fd", command=lambda: self.toggle_group("bfs"), **btn_toggle_config)
        self.btn_bfs_toggle.pack(fill=tk.X)
        
        self.bfs_sub_frame = tk.Frame(self.bfs_container, bg="#ffffff")
        
        self.btn_bfs1 = tk.Button(self.bfs_sub_frame, text="Tiếp cận 1 (Late)", bg="#f0f7ff", command=lambda: self.run_algo(bfs1.solve, "BFS Tiếp cận 1"), **btn_sub_config)
        self.btn_bfs1.pack(fill=tk.X, pady=2, padx=10)
        
        self.btn_bfs2 = tk.Button(self.bfs_sub_frame, text="Tiếp cận 2 (Early)", bg="#f0f7ff", command=lambda: self.run_algo(bfs2.solve, "BFS Tiếp cận 2"), **btn_sub_config)
        self.btn_bfs2.pack(fill=tk.X, pady=2, padx=10)
        
        # --- 2. Nhóm DFS ---
        self.dfs_container = tk.Frame(left_frame, bg="#ffffff")
        self.dfs_container.pack(fill=tk.X, pady=3)
        
        self.btn_dfs_toggle = tk.Button(self.dfs_container, text="🌸 DFS Search  ▸", bg="#fce4ec", command=lambda: self.toggle_group("dfs"), **btn_toggle_config)
        self.btn_dfs_toggle.pack(fill=tk.X)
        
        self.dfs_sub_frame = tk.Frame(self.dfs_container, bg="#ffffff")
        
        self.btn_dfs1 = tk.Button(self.dfs_sub_frame, text="Tiếp cận 1 (Late)", bg="#fff0f5", command=lambda: self.run_algo(dfs1.solve, "DFS Tiếp cận 1"), **btn_sub_config)
        self.btn_dfs1.pack(fill=tk.X, pady=2, padx=10)
        
        self.btn_dfs2 = tk.Button(self.dfs_sub_frame, text="Tiếp cận 2 (Early)", bg="#fff0f5", command=lambda: self.run_algo(dfs2.solve, "DFS Tiếp cận 2"), **btn_sub_config)
        self.btn_dfs2.pack(fill=tk.X, pady=2, padx=10)
        
        # --- 3. Nhóm IDS ---
        self.ids_container = tk.Frame(left_frame, bg="#ffffff")
        self.ids_container.pack(fill=tk.X, pady=3)
        
        self.btn_ids_toggle = tk.Button(self.ids_container, text="🌱 IDS Search  ▸", bg="#e8f5e9", command=lambda: self.toggle_group("ids"), **btn_toggle_config)
        self.btn_ids_toggle.pack(fill=tk.X)
        
        self.ids_sub_frame = tk.Frame(self.ids_container, bg="#ffffff")
        
        self.btn_ids1 = tk.Button(self.ids_sub_frame, text="Tiếp cận 1 (Late)", bg="#f1fcf2", command=lambda: self.run_algo(ids1.solve, "IDS Tiếp cận 1"), **btn_sub_config)
        self.btn_ids1.pack(fill=tk.X, pady=2, padx=10)
        
        self.btn_ids2 = tk.Button(self.ids_sub_frame, text="Tiếp cận 2 (Early)", bg="#f1fcf2", command=lambda: self.run_algo(ids2.solve, "IDS Tiếp cận 2"), **btn_sub_config)
        self.btn_ids2.pack(fill=tk.X, pady=2, padx=10)
        
        # --- 4. Nhóm Leo Núi (Hill Climbing) ---
        self.hill_container = tk.Frame(left_frame, bg="#ffffff")
        self.hill_container.pack(fill=tk.X, pady=3)
        
        self.btn_hill_toggle = tk.Button(self.hill_container, text="⛰️ Leo Núi Search  ▸", bg="#fff3e0", command=lambda: self.toggle_group("hill"), **btn_toggle_config)
        self.btn_hill_toggle.pack(fill=tk.X)
        
        self.hill_sub_frame = tk.Frame(self.hill_container, bg="#ffffff")
        
        self.btn_hill_simple = tk.Button(self.hill_sub_frame, text="Leo núi Đơn giản", bg="#fffdf0", command=lambda: self.run_algo(hill_climbing.solve_simple, "Leo núi Đơn giản"), **btn_sub_config)
        self.btn_hill_simple.pack(fill=tk.X, pady=2, padx=10)
        
        self.btn_hill_steepest = tk.Button(self.hill_sub_frame, text="Leo núi Dốc nhất", bg="#fffdf0", command=lambda: self.run_algo(hill_climbing.solve_steepest, "Leo núi Dốc nhất"), **btn_sub_config)
        self.btn_hill_steepest.pack(fill=tk.X, pady=2, padx=10)
        
        self.btn_hill_stochastic = tk.Button(self.hill_sub_frame, text="Leo núi Ngẫu nhiên", bg="#fffdf0", command=lambda: self.run_algo(hill_climbing.solve_stochastic, "Leo núi Ngẫu nhiên"), **btn_sub_config)
        self.btn_hill_stochastic.pack(fill=tk.X, pady=2, padx=10)
        
        # --- 5. Nhóm Heuristic / Khác ---
        self.others_container = tk.Frame(left_frame, bg="#ffffff")
        self.others_container.pack(fill=tk.X, pady=3)
        
        self.btn_others_toggle = tk.Button(self.others_container, text="⚡ Heuristic / Khác  ▸", bg="#f3e5f5", command=lambda: self.toggle_group("others"), **btn_toggle_config)
        self.btn_others_toggle.pack(fill=tk.X)
        
        self.others_sub_frame = tk.Frame(self.others_container, bg="#ffffff")
        
        self.btn_ucs = tk.Button(self.others_sub_frame, text="UCS Search", bg="#faf5ff", command=lambda: self.run_algo(ucs.solve, "UCS"), **btn_sub_config)
        self.btn_ucs.pack(fill=tk.X, pady=2, padx=10)
        
        self.btn_greedy = tk.Button(self.others_sub_frame, text="Greedy Best-First", bg="#faf5ff", command=lambda: self.run_algo(greedy.solve, "Greedy Best-First"), **btn_sub_config)
        self.btn_greedy.pack(fill=tk.X, pady=2, padx=10)
        
        self.btn_astar = tk.Button(self.others_sub_frame, text="A* Search", bg="#faf5ff", command=lambda: self.run_algo(Astar.solve, "A* Search"), **btn_sub_config)
        self.btn_astar.pack(fill=tk.X, pady=2, padx=10)
        
        self.btn_idastar = tk.Button(self.others_sub_frame, text="IDA* Search", bg="#faf5ff", command=lambda: self.run_algo(idastar.solve, "IDA* Search"), **btn_sub_config)
        self.btn_idastar.pack(fill=tk.X, pady=2, padx=10)
        
        tk.Frame(left_frame, height=2, bg="#cccccc").pack(fill=tk.X, pady=10, padx=10)
        
        tk.Label(left_frame, text="TỐC ĐỘ (ms/bước)", font=("Segoe UI", 10, "bold"), bg="#ffffff").pack(pady=(5, 0))
        self.speed_scale = tk.Scale(left_frame, from_=50, to=1000, orient=tk.HORIZONTAL, bg="#ffffff", length=180, resolution=50, cursor="hand2")
        self.speed_scale.set(300)
        self.speed_scale.pack(pady=5)
        
        tk.Frame(left_frame, height=2, bg="#cccccc").pack(fill=tk.X, pady=10, padx=10)
        
        self.btn_reset = tk.Button(left_frame, text="🔄 Reset Trạng Thái", bg="#ffebee", command=self.reset_state, **btn_config)
        self.btn_reset.pack(pady=10)
        
        # Khu vực Phải (Log sự kiện & Thống kê)
        right_frame = tk.Frame(self.root, width=320, bg="#ffffff", relief="ridge", borderwidth=2)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        
        tk.Label(right_frame, text="THỐNG KÊ THUẬT TOÁN", font=("Segoe UI", 12, "bold"), bg="#ffffff").pack(pady=(10, 5))
        
        stats_frame = tk.Frame(right_frame, bg="#f8f9fa", relief="sunken", borderwidth=1)
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.lbl_path_cost = tk.Label(stats_frame, text="Số bước đi (Cost): -", font=("Segoe UI", 10), bg="#f8f9fa", anchor="w")
        self.lbl_path_cost.pack(fill=tk.X, padx=10, pady=2)
        
        self.lbl_nodes = tk.Label(stats_frame, text="Số Node đã duyệt: -", font=("Segoe UI", 10), bg="#f8f9fa", anchor="w")
        self.lbl_nodes.pack(fill=tk.X, padx=10, pady=2)
        
        self.lbl_time = tk.Label(stats_frame, text="Thời gian chạy: -", font=("Segoe UI", 10), bg="#f8f9fa", anchor="w")
        self.lbl_time.pack(fill=tk.X, padx=10, pady=2)
        
        tk.Label(right_frame, text="LỊCH SỬ HÀNH ĐỘNG", font=("Segoe UI", 12, "bold"), bg="#ffffff").pack(pady=(15, 5))
        self.log_text = scrolledtext.ScrolledText(right_frame, width=40, font=("Consolas", 10), bg="#fafafa")
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Khu vực Giữa (Trực quan hóa Grid) & Dưới (Console)
        center_frame = tk.Frame(self.root, bg="#f4f4f4")
        center_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(center_frame, text="TRỰC QUAN HÓA GRID 4x4", font=("Segoe UI", 14, "bold"), bg="#f4f4f4").pack(pady=10)
        tk.Label(center_frame, text="(Click vào ô để thêm/xóa bụi)", font=("Segoe UI", 10, "italic"), bg="#f4f4f4", fg="#555555").pack(pady=(0, 10))
        
        self.canvas_size = 400
        self.cell_size = self.canvas_size // 4
        self.canvas = tk.Canvas(center_frame, width=self.canvas_size, height=self.canvas_size, bg="#ffffff", highlightthickness=2, highlightbackground="#333333", cursor="hand2")
        self.canvas.pack(pady=5)
        
        # Bind click event for interactive grid
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        
        tk.Label(center_frame, text="MA TRẬN TRẠNG THÁI HIỆN TẠI", font=("Segoe UI", 12, "bold"), bg="#f4f4f4").pack(pady=(15,5))
        self.matrix_console = scrolledtext.ScrolledText(center_frame, width=45, height=10, font=("Consolas", 16, "bold"), bg="#282c34", fg="#98c379")
        self.matrix_console.pack(pady=5)
        
    def toggle_group(self, name):
        if name == "bfs":
            if self.group_states["bfs"]:
                self.bfs_sub_frame.pack_forget()
                self.btn_bfs_toggle.config(text="🔍 BFS Search  ▸")
                self.group_states["bfs"] = False
            else:
                self.bfs_sub_frame.pack(fill=tk.X, pady=2)
                self.btn_bfs_toggle.config(text="🔍 BFS Search  ▾")
                self.group_states["bfs"] = True
        elif name == "dfs":
            if self.group_states["dfs"]:
                self.dfs_sub_frame.pack_forget()
                self.btn_dfs_toggle.config(text="🌸 DFS Search  ▸")
                self.group_states["dfs"] = False
            else:
                self.dfs_sub_frame.pack(fill=tk.X, pady=2)
                self.btn_dfs_toggle.config(text="🌸 DFS Search  ▾")
                self.group_states["dfs"] = True
        elif name == "ids":
            if self.group_states["ids"]:
                self.ids_sub_frame.pack_forget()
                self.btn_ids_toggle.config(text="🌱 IDS Search  ▸")
                self.group_states["ids"] = False
            else:
                self.ids_sub_frame.pack(fill=tk.X, pady=2)
                self.btn_ids_toggle.config(text="🌱 IDS Search  ▾")
                self.group_states["ids"] = True
        elif name == "hill":
            if self.group_states["hill"]:
                self.hill_sub_frame.pack_forget()
                self.btn_hill_toggle.config(text="⛰️ Leo Núi Search  ▸")
                self.group_states["hill"] = False
            else:
                self.hill_sub_frame.pack(fill=tk.X, pady=2)
                self.btn_hill_toggle.config(text="⛰️ Leo Núi Search  ▾")
                self.group_states["hill"] = True
        elif name == "others":
            if self.group_states["others"]:
                self.others_sub_frame.pack_forget()
                self.btn_others_toggle.config(text="⚡ Heuristic / Khác  ▸")
                self.group_states["others"] = False
            else:
                self.others_sub_frame.pack(fill=tk.X, pady=2)
                self.btn_others_toggle.config(text="⚡ Heuristic / Khác  ▾")
                self.group_states["others"] = True

    def set_buttons_state(self, state):
        self.btn_bfs_toggle.config(state=state)
        self.btn_bfs1.config(state=state)
        self.btn_bfs2.config(state=state)
        
        self.btn_dfs_toggle.config(state=state)
        self.btn_dfs1.config(state=state)
        self.btn_dfs2.config(state=state)
        
        self.btn_ids_toggle.config(state=state)
        self.btn_ids1.config(state=state)
        self.btn_ids2.config(state=state)
        
        self.btn_hill_toggle.config(state=state)
        self.btn_hill_simple.config(state=state)
        self.btn_hill_steepest.config(state=state)
        self.btn_hill_stochastic.config(state=state)
        
        self.btn_others_toggle.config(state=state)
        self.btn_ucs.config(state=state)
        self.btn_greedy.config(state=state)
        self.btn_astar.config(state=state)
        self.btn_idastar.config(state=state)
        
        self.btn_reset.config(state=state)
        self.speed_scale.config(state=state)
        
    def reset_state(self):
        if self.is_running:
            return
            
        self.log_text.delete(1.0, tk.END)
        self.matrix_console.delete(1.0, tk.END)
        
        self.lbl_path_cost.config(text="Số bước đi (Cost): -")
        self.lbl_nodes.config(text="Số Node đã duyệt: -")
        self.lbl_time.config(text="Thời gian chạy: -")
        
        self.current_pos = (0, 0)
        self.current_dirts = {(1, 2), (2, 0), (3, 1), (3, 3)}
        
        self.draw_grid()
        self.update_matrix_console()
        self.log("Hệ thống đã reset. Sẵn sàng hoạt động.")
        
    def on_canvas_click(self, event):
        if self.is_running:
            return
        
        c = event.x // self.cell_size
        r = event.y // self.cell_size
        
        if 0 <= r < 4 and 0 <= c < 4:
            if (r, c) in self.current_dirts:
                self.current_dirts.remove((r, c))
            else:
                self.current_dirts.add((r, c))
            self.draw_grid()
            self.update_matrix_console()
        
    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        
    def get_path_frames(self, goal_node):
        path = []
        curr = goal_node
        while curr:
            path.append(curr)
            curr = curr.parent
        path.reverse()
        
        frames = []
        for node in path:
            pos = node.state[0]
            dirts = node.state[1]
            action = node.action
            
            if action:
                action_text = {"R": "RIGHT", "D": "DOWN", "L": "LEFT", "U": "UP"}.get(action, action)
                msg = f"Máy đang di chuyển {action_text} đến vị trí {list(pos)}"
            else:
                msg = f"Bắt đầu tại vị trí {list(pos)}"
                
            frames.append({
                "robot_pos": pos,
                "dirts": dirts,
                "action": action,
                "log": msg
            })
        return frames

    def run_algo(self, solve_func, algo_name):
        if self.is_running:
            return
            
        self.log_text.delete(1.0, tk.END)
        self.lbl_path_cost.config(text="Số bước đi (Cost): Đang tính...")
        self.lbl_nodes.config(text="Số Node đã duyệt: Đang tính...")
        self.lbl_time.config(text="Thời gian chạy: Đang tính...")
        
        self.log(f"--- ĐANG CHẠY {algo_name.upper()} ---")
        self.set_buttons_state(tk.DISABLED)
        self.is_running = True
        
        # Gọi thuật toán với tham số vị trí bụi động
        goal_node, node_count, exec_time = solve_func(self.current_dirts)
        
        self.lbl_nodes.config(text=f"Số Node đã duyệt: {node_count}")
        self.lbl_time.config(text=f"Thời gian chạy: {exec_time:.5f}s")
        
        if not goal_node:
            self.log("❌ Không tìm thấy đường đi!")
            self.lbl_path_cost.config(text="Số bước đi (Cost): Không có")
            self.is_running = False
            self.set_buttons_state(tk.NORMAL)
            return
            
        frames = self.get_path_frames(goal_node)
        
        # Kiểm tra xem có thực sự sạch hết bụi hay không (Goal thực sự)
        final_dirts = goal_node.state[1]
        is_goal_reached = len(final_dirts) == 0
        
        if is_goal_reached:
            self.log(f"🎉 Đã tìm thấy đường đi! Lộ trình: {len(frames)-1} bước.")
            self.lbl_path_cost.config(text=f"Số bước đi (Cost): {len(frames)-1}")
        else:
            self.log(f"⚠️ THUẬT TOÁN BỊ KẸT / DỪNG LẠI! Đã đi được: {len(frames)-1} bước.")
            self.log(f"   Còn lại {len(final_dirts)} ô bụi chưa quét.")
            if "leo núi" in algo_name.lower():
                self.log("   👉 Lý do: Đã rơi vào Cực tiểu địa phương (Local Minimum) hoặc Cao nguyên, không có hướng đi nào làm sạch thêm bụi.")
            self.lbl_path_cost.config(text=f"{len(frames)-1} bước (Bị kẹt!)")
            
        # Bắt đầu hiệu ứng trượt mượt mà
        self.animate_frames(frames, 0, is_goal_reached)
        
    def animate_frames(self, frames, index, is_goal_reached=True):
        if index >= len(frames):
            if is_goal_reached:
                self.log("\n✨ HOÀN THÀNH LỘ TRÌNH (SẠCH BỤI)!")
                messagebox.showinfo("Thành công", "Đã quét sạch toàn bộ bụi!")
            else:
                self.log("\n⚠️ THUẬT TOÁN ĐÃ DỪNG (BỊ KẸT / CỰC TIỂU ĐỊA PHƯƠNG)!")
                messagebox.showwarning("Cảnh báo", f"Thuật toán bị kẹt hoặc đã dừng!\nCòn lại {len(self.current_dirts)} ô bụi chưa được quét.")
            self.is_running = False
            self.set_buttons_state(tk.NORMAL)
            self.draw_grid() # Cleanup
            return
            
        frame = frames[index]
        next_pos = frame["robot_pos"]
        self.current_dirts = set(frame["dirts"])
        
        self.draw_background()
        self.smooth_move(self.current_pos, next_pos, frame, frames, index, is_goal_reached)
        
    def smooth_move(self, start_pos, end_pos, frame, frames, index, is_goal_reached=True):
        if start_pos == end_pos:
            self.current_pos = end_pos
            self.update_matrix_console()
            self.log("➡️ " + frame["log"])
            speed = self.speed_scale.get()
            self.root.after(speed, self.animate_frames, frames, index + 1, is_goal_reached)
            return
            
        sr, sc = start_pos
        er, ec = end_pos
        
        steps = 15 # Số lượng frame cho mỗi bước nhảy
        speed = self.speed_scale.get()
        delay_per_step = speed // steps
        if delay_per_step < 1: delay_per_step = 1
        
        dr = (er - sr) / steps
        dc = (ec - sc) / steps
        
        self.log("➡️ " + frame["log"])
        self.perform_step(sr, sc, dr, dc, 0, steps, end_pos, frames, index, is_goal_reached)
        
    def perform_step(self, r, c, dr, dc, step_idx, total_steps, end_pos, frames, index, is_goal_reached=True):
        if step_idx < total_steps:
            r += dr
            c += dc
            self.draw_robot(r, c)
            speed = self.speed_scale.get()
            delay = max(1, speed // total_steps)
            self.root.after(delay, self.perform_step, r, c, dr, dc, step_idx + 1, total_steps, end_pos, frames, index, is_goal_reached)
        else:
            self.current_pos = end_pos
            self.draw_robot(end_pos[0], end_pos[1])
            self.update_matrix_console()
            self.root.after(10, self.animate_frames, frames, index + 1, is_goal_reached)

    def draw_grid(self):
        self.canvas.delete("all")
        self.draw_background()
        self.draw_robot(self.current_pos[0], self.current_pos[1])
        
    def draw_background(self):
        self.canvas.delete("bg")
        self.canvas.delete("dirt")
        for r in range(4):
            for c in range(4):
                x0 = c * self.cell_size
                y0 = r * self.cell_size
                x1 = x0 + self.cell_size
                y1 = y0 + self.cell_size
                
                # Nền ô (Trắng/Xanh nhạt hoặc Xám nhạt)
                bg_color = "#ffffff" if (r, c) not in self.current_dirts else "#f3f4f6"
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=bg_color, outline="#e5e7eb", width=1.5, tags="bg")
                
                # Biểu tượng bụi bẩn nghệ thuật
                if (r, c) in self.current_dirts:
                    self.canvas.create_oval(x0 + 15, y0 + 15, x1 - 15, y1 - 15, fill="#f1f5f9", outline="#cbd5e1", width=1, tags="dirt")
                    self.canvas.create_oval(x0 + 25, y0 + 25, x0 + 29, y0 + 29, fill="#94a3b8", outline="", tags="dirt")
                    self.canvas.create_oval(x0 + 70, y0 + 30, x0 + 74, y0 + 34, fill="#94a3b8", outline="", tags="dirt")
                    self.canvas.create_oval(x0 + 30, y0 + 68, x0 + 34, y0 + 72, fill="#94a3b8", outline="", tags="dirt")
                    self.canvas.create_oval(x0 + 68, y0 + 68, x0 + 72, y0 + 72, fill="#94a3b8", outline="", tags="dirt")
                    self.canvas.create_text(x0 + self.cell_size/2, y0 + self.cell_size/2, text="💨", font=("Segoe UI Emoji", 26), tags="dirt")
        
        self.canvas.tag_lower("dirt")
        self.canvas.tag_lower("bg")
        
    def draw_robot(self, r, c):
        self.canvas.delete("robot")
        x0 = c * self.cell_size
        y0 = r * self.cell_size
        x1 = x0 + self.cell_size
        y1 = y0 + self.cell_size
        
        # Modern Roomba Design
        # Outer shell
        self.canvas.create_oval(x0 + 15, y0 + 15, x1 - 15, y1 - 15, fill="#2c3e50", outline="#1a252f", width=2, tags="robot")
        # Inner circle
        self.canvas.create_oval(x0 + 25, y0 + 25, x1 - 25, y1 - 25, fill="#34495e", outline="#3498db", width=2, tags="robot")
        # LED indicator (green if active)
        led_color = "#2ecc71" if self.is_running else "#e74c3c"
        self.canvas.create_oval(x0 + 45, y0 + 45, x1 - 45, y1 - 45, fill=led_color, outline="#27ae60", tags="robot")

    def update_matrix_console(self):
        self.matrix_console.delete(1.0, tk.END)
        matrix_str = "\n"
        for r in range(4):
            row_chars = []
            for c in range(4):
                if (r, c) == self.current_pos:
                    row_chars.append("[ X ]")
                elif (r, c) in self.current_dirts:
                    row_chars.append("[ 1 ]")
                else:
                    row_chars.append("[ 0 ]")
            matrix_str += "    " + "  ".join(row_chars) + "\n\n"
        self.matrix_console.insert(tk.END, matrix_str)

if __name__ == "__main__":
    root = tk.Tk()
    app = VacuumVisualizer(root)
    root.mainloop()
