# -*- coding: utf-8 -*-
"""
ui.py
Thiết kế giao diện đồ họa Tkinter hiện đại, mượt mà và trực quan cho game Caro AI.
Hỗ trợ chạy thuật toán AI ở luồng nền (background thread) để tránh treo giao diện.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from typing import Optional, Tuple

from game_logic import CaroBoard
from minimax import MinimaxAI
from alpha_beta import AlphaBetaAI
from expectimax import ExpectimaxAI

class CaroGUI:
    def __init__(self, master: tk.Tk):
        self.master = master
        self.master.title("Caro AI - Minimax, Alpha-Beta & Expectimax")
        self.master.geometry("1050x720")
        self.master.resizable(False, False)
        
        # Thiết lập màu sắc hiện đại
        self.COLOR_BG = "#1e293b"          # Slate 800 (nền chính)
        self.COLOR_SIDEBAR = "#0f172a"     # Slate 900 (nền sidebar)
        self.COLOR_BOARD_BG = "#f8fafc"    # Slate 50 (nền bàn cờ)
        self.COLOR_GRID = "#cbd5e1"        # Slate 300 (đường lưới)
        self.COLOR_X = "#2563eb"           # Blue 600 (Người chơi X)
        self.COLOR_O = "#dc2626"           # Red 600 (AI O)
        self.COLOR_HIGHLIGHT = "#bbf7d0"   # Green 200 (Nổi bật ô vừa đánh)
        self.COLOR_TEXT_LIGHT = "#f1f5f9"  # Slate 100
        
        self.master.configure(bg=self.COLOR_BG)

        # Khởi tạo dữ liệu game mặc định
        self.board_size = 10
        self.to_win = 5
        self.board = CaroBoard(self.board_size, self.to_win)
        
        self.player_symbol = "X"
        self.ai_symbol = "O"
        self.current_turn = "X"  # 'X' đi trước
        self.game_over = False
        
        # Thống kê điểm số
        self.scores = {"X": 0, "O": 0, "Draws": 0}
        
        # Lưu vết nước đi cuối cùng để highlight
        self.last_move: Optional[Tuple[int, int]] = None
        
        # Trạng thái luồng AI
        self.ai_thread: Optional[threading.Thread] = None
        self.ai_thinking = False
        self.ai_result: Optional[Tuple[int, int]] = None
        self.ai_nodes_evaluated = 0
        self.ai_calc_time = 0.0

        # Tạo giao diện
        self._create_widgets()
        self._reset_game()

    def _create_widgets(self):
        # 1. Sidebar Panel (Trái)
        sidebar = tk.Frame(self.master, width=320, bg=self.COLOR_SIDEBAR, padx=15, pady=15)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        # Tiêu đề game
        title_label = tk.Label(
            sidebar, 
            text="CARO AI", 
            font=("Segoe UI", 24, "bold"), 
            bg=self.COLOR_SIDEBAR, 
            fg="#60a5fa"
        )
        title_label.pack(anchor=tk.W, pady=(0, 5))
        
        sub_title = tk.Label(
            sidebar, 
            text="Minimax - AlphaBeta - Expectimax", 
            font=("Segoe UI", 9, "italic"), 
            bg=self.COLOR_SIDEBAR, 
            fg="#94a3b8"
        )
        sub_title.pack(anchor=tk.W, pady=(0, 20))

        # --- CẤU HÌNH BÀN CỜ ---
        lbl_sec_1 = tk.Label(sidebar, text="CẤU HÌNH GAME", font=("Segoe UI", 11, "bold"), bg=self.COLOR_SIDEBAR, fg="#f1f5f9")
        lbl_sec_1.pack(anchor=tk.W, pady=(10, 5))

        # Chọn kích thước bàn cờ
        tk.Label(sidebar, text="Kích thước bàn cờ & Luật thắng:", font=("Segoe UI", 9), bg=self.COLOR_SIDEBAR, fg="#cbd5e1").pack(anchor=tk.W)
        self.combo_size = ttk.Combobox(sidebar, values=["3x3 (Thắng 3)", "5x5 (Thắng 4)", "10x10 (Thắng 5)"], state="readonly")
        self.combo_size.set("10x10 (Thắng 5)")
        self.combo_size.pack(fill=tk.X, pady=(0, 10))
        self.combo_size.bind("<<ComboboxSelected>>", self._on_config_change)

        # Chọn thuật toán AI
        tk.Label(sidebar, text="Thuật toán AI:", font=("Segoe UI", 9), bg=self.COLOR_SIDEBAR, fg="#cbd5e1").pack(anchor=tk.W)
        self.combo_algo = ttk.Combobox(sidebar, values=["Minimax", "Alpha-Beta Pruning", "Expectimax"], state="readonly")
        self.combo_algo.set("Alpha-Beta Pruning")
        self.combo_algo.pack(fill=tk.X, pady=(0, 10))
        self.combo_algo.bind("<<ComboboxSelected>>", self._on_config_change)

        # Chọn độ sâu tìm kiếm (Depth)
        tk.Label(sidebar, text="Độ sâu tìm kiếm (Depth):", font=("Segoe UI", 9), bg=self.COLOR_SIDEBAR, fg="#cbd5e1").pack(anchor=tk.W)
        self.combo_depth = ttk.Combobox(sidebar, values=["1", "2", "3", "4", "5"], state="readonly")
        self.combo_depth.set("3")
        self.combo_depth.pack(fill=tk.X, pady=(0, 10))
        
        # Nhãn cảnh báo độ sâu lớn
        self.lbl_warning = tk.Label(
            sidebar, 
            text="Khuyến nghị: Bàn cờ 10x10 nên để Depth <= 3.", 
            font=("Segoe UI", 8, "italic"), 
            bg=self.COLOR_SIDEBAR, 
            fg="#f59e0b",
            wraplength=290,
            justify=tk.LEFT
        )
        self.lbl_warning.pack(anchor=tk.W, pady=(0, 15))

        # Chọn người đi trước
        tk.Label(sidebar, text="Đi trước:", font=("Segoe UI", 9), bg=self.COLOR_SIDEBAR, fg="#cbd5e1").pack(anchor=tk.W)
        self.combo_first = ttk.Combobox(sidebar, values=["Người chơi (X)", "AI (O)"], state="readonly")
        self.combo_first.set("Người chơi (X)")
        self.combo_first.pack(fill=tk.X, pady=(0, 15))

        # Các nút điều khiển
        self.btn_new_game = tk.Button(
            sidebar, 
            text="Ván Mới", 
            font=("Segoe UI", 10, "bold"), 
            bg="#2563eb", 
            fg="white", 
            activebackground="#1d4ed8", 
            activeforeground="white",
            bd=0, 
            pady=8,
            cursor="hand2",
            command=self._reset_game
        )
        self.btn_new_game.pack(fill=tk.X, pady=5)

        # --- THỐNG KÊ ĐIỂM SỐ ---
        lbl_sec_2 = tk.Label(sidebar, text="BẢNG ĐIỂM", font=("Segoe UI", 11, "bold"), bg=self.COLOR_SIDEBAR, fg="#f1f5f9")
        lbl_sec_2.pack(anchor=tk.W, pady=(20, 5))

        self.lbl_scoreboard = tk.Label(
            sidebar, 
            text="Bạn (X): 0  |  AI (O): 0  |  Hòa: 0", 
            font=("Segoe UI", 10, "bold"), 
            bg="#1e293b", 
            fg="#38bdf8",
            pady=6,
            bd=1,
            relief=tk.SOLID
        )
        self.lbl_scoreboard.pack(fill=tk.X, pady=(0, 15))

        # --- THÔNG TIN HIỆU NĂNG AI ---
        lbl_sec_3 = tk.Label(sidebar, text="HIỆU NĂNG AI", font=("Segoe UI", 11, "bold"), bg=self.COLOR_SIDEBAR, fg="#f1f5f9")
        lbl_sec_3.pack(anchor=tk.W, pady=(10, 5))

        self.lbl_perf = tk.Label(
            sidebar, 
            text="Trạng thái đã duyệt: 0\nThời gian tính: 0.00s", 
            font=("Consolas", 9), 
            bg=self.COLOR_SIDEBAR, 
            fg="#a1a1aa",
            justify=tk.LEFT
        )
        self.lbl_perf.pack(anchor=tk.W, pady=5)

        # 2. Main Game Panel (Phải)
        game_panel = tk.Frame(self.master, bg=self.COLOR_BG, padx=20, pady=20)
        game_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Dòng trạng thái lượt đi
        self.lbl_status = tk.Label(
            game_panel, 
            text="Lượt chơi của bạn (X)", 
            font=("Segoe UI", 14, "bold"), 
            bg=self.COLOR_BG, 
            fg=self.COLOR_TEXT_LIGHT
        )
        self.lbl_status.pack(pady=(0, 15))

        # Khung bàn cờ Canvas
        self.canvas_size = 580
        self.canvas = tk.Canvas(
            game_panel, 
            width=self.canvas_size, 
            height=self.canvas_size, 
            bg=self.COLOR_BOARD_BG,
            highlightthickness=1,
            highlightbackground="#cbd5e1"
        )
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self._on_canvas_click)

    def _on_config_change(self, event=None):
        """Thay đổi cảnh báo khi người dùng cấu hình độ sâu hoặc kích thước."""
        size_str = self.combo_size.get()
        if "10x10" in size_str:
            self.lbl_warning.configure(
                text="Khuyến nghị: Bàn cờ 10x10 nên để Depth <= 3. Tránh chọn Depth > 3 để không bị đơ/chờ lâu.", 
                fg="#f59e0b"
            )
        elif "5x5" in size_str:
            self.lbl_warning.configure(
                text="Khuyến nghị: Bàn cờ 5x5 có thể chạy tốt ở Depth <= 4.", 
                fg="#10b981"
            )
        else:
            self.lbl_warning.configure(
                text="Khuyến nghị: Bàn cờ 3x3 có thể chạy ở độ sâu tối đa (Depth = 5).", 
                fg="#10b981"
            )

    def _reset_game(self):
        """Khởi động lại ván cờ mới với các thiết lập hiện tại."""
        if self.ai_thinking:
            messagebox.showwarning("Cảnh báo", "AI đang suy nghĩ, vui lòng đợi xong lượt đi.")
            return

        # 1. Đọc cấu hình
        size_str = self.combo_size.get()
        if "3x3" in size_str:
            self.board_size = 3
            self.to_win = 3
        elif "5x5" in size_str:
            self.board_size = 5
            self.to_win = 4
        else:
            self.board_size = 10
            self.to_win = 5

        self.board = CaroBoard(self.board_size, self.to_win)
        self.last_move = None
        self.game_over = False
        
        # Xác định ai đi trước
        first_str = self.combo_first.get()
        if "AI" in first_str:
            self.current_turn = "O"
        else:
            self.current_turn = "X"

        # Cập nhật giao diện
        self._draw_grid()
        self._update_status()

        # Nếu AI đi trước, kích hoạt lượt của AI
        if self.current_turn == "O":
            self._trigger_ai_move()

    def _draw_grid(self):
        """Vẽ lại toàn bộ lưới bàn cờ và các quân cờ."""
        self.canvas.delete("all")
        self.cell_size = self.canvas_size / self.board_size

        # Vẽ các ô highlight nếu có nước đi cuối cùng
        if self.last_move is not None:
            r, c = self.last_move
            x1, y1 = c * self.cell_size, r * self.cell_size
            x2, y2 = x1 + self.cell_size, y1 + self.cell_size
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.COLOR_HIGHLIGHT, outline="")

        # Vẽ các đường lưới dọc và ngang
        for i in range(self.board_size + 1):
            coord = i * self.cell_size
            # Đường dọc
            self.canvas.create_line(coord, 0, coord, self.canvas_size, fill=self.COLOR_GRID, width=1)
            # Đường ngang
            self.canvas.create_line(0, coord, self.canvas_size, coord, fill=self.COLOR_GRID, width=1)

        # Vẽ các quân cờ hiện tại
        for r in range(self.board_size):
            for c in range(self.board_size):
                stone = self.board.grid[r][c]
                if stone == "X":
                    self._draw_x(r, c)
                elif stone == "O":
                    self._draw_o(r, c)

    def _draw_x(self, r: int, c: int):
        """Vẽ quân cờ X tại ô (r, c) với hiệu ứng bóng bẩy."""
        offset = self.cell_size * 0.18
        x1 = c * self.cell_size + offset
        y1 = r * self.cell_size + offset
        x2 = (c + 1) * self.cell_size - offset
        y2 = (r + 1) * self.cell_size - offset
        
        self.canvas.create_line(x1, y1, x2, y2, fill=self.COLOR_X, width=4, capstyle=tk.ROUND)
        self.canvas.create_line(x2, y1, x1, y2, fill=self.COLOR_X, width=4, capstyle=tk.ROUND)

    def _draw_o(self, r: int, c: int):
        """Vẽ quân cờ O tại ô (r, c) tròn và sắc nét."""
        offset = self.cell_size * 0.18
        x1 = c * self.cell_size + offset
        y1 = r * self.cell_size + offset
        x2 = (c + 1) * self.cell_size - offset
        y2 = (r + 1) * self.cell_size - offset
        
        self.canvas.create_oval(x1, y1, x2, y2, outline=self.COLOR_O, width=4)

    def _on_canvas_click(self, event):
        """Xử lý sự kiện người chơi click chuột vào ô cờ trên Canvas."""
        if self.game_over or self.ai_thinking or self.current_turn != "X":
            return

        # Tính toán tọa độ ô cờ từ tọa độ pixel
        c = int(event.x // self.cell_size)
        r = int(event.y // self.cell_size)

        if 0 <= r < self.board_size and 0 <= c < self.board_size:
            if self.board.grid[r][c] is None:
                # Đánh nước đi của người chơi
                self.board.make_move(r, c, "X")
                self.last_move = (r, c)
                self._draw_grid()
                
                # Kiểm tra kết quả sau nước đi
                if self._check_game_end():
                    return
                
                # Chuyển lượt sang AI
                self.current_turn = "O"
                self._update_status()
                self._trigger_ai_move()

    def _trigger_ai_move(self):
        """Kích hoạt một luồng phụ để AI tính toán, tránh treo giao diện chính."""
        self.ai_thinking = True
        self.ai_result = None
        self.ai_nodes_evaluated = 0
        self.ai_calc_time = 0.0

        # Lấy các thiết lập thuật toán
        algo_name = self.combo_algo.get()
        depth = int(self.combo_depth.get())

        # Khởi tạo đối tượng AI tương ứng
        if algo_name == "Minimax":
            ai_agent = MinimaxAI(depth)
        elif algo_name == "Expectimax":
            ai_agent = ExpectimaxAI(depth)
        else:
            ai_agent = AlphaBetaAI(depth)

        # Định nghĩa hàm chạy trong luồng nền
        def ai_search_job():
            start_time = time.time()
            # Sao chép bàn cờ để AI tìm kiếm độc lập
            board_copy = self.board.copy()
            best_move = ai_agent.get_best_move(board_copy, self.ai_symbol)
            self.ai_calc_time = time.time() - start_time
            self.ai_nodes_evaluated = ai_agent.nodes_evaluated
            self.ai_result = best_move
            self.ai_thinking = False

        # Chạy luồng
        self.ai_thread = threading.Thread(target=ai_search_job)
        self.ai_thread.daemon = True
        self.ai_thread.start()

        # Bắt đầu kiểm tra xem luồng AI đã tính toán xong chưa
        self.master.after(50, self._check_ai_status)

    def _check_ai_status(self):
        """Kiểm tra định kỳ trạng thái của luồng tính toán AI."""
        if self.ai_thinking:
            # Nếu AI vẫn đang tính, tiếp tục kiểm tra sau 50ms
            self.master.after(50, self._check_ai_status)
        else:
            # AI đã hoàn thành, thực hiện nước đi
            if self.ai_result is not None:
                r, c = self.ai_result
                self.board.make_move(r, c, self.ai_symbol)
                self.last_move = (r, c)
                self._draw_grid()

                # Cập nhật nhãn hiệu năng
                self.lbl_perf.configure(
                    text=f"Trạng thái đã duyệt: {self.ai_nodes_evaluated}\nThời gian tính: {self.ai_calc_time:.3f}s"
                )

                if self._check_game_end():
                    return

                # Trả lượt về cho người chơi
                self.current_turn = "X"
                self._update_status()
            else:
                # Nếu không tìm thấy nước đi (hiếm khi xảy ra trừ khi bàn cờ đầy)
                if not self._check_game_end():
                    self.current_turn = "X"
                    self._update_status()

    def _check_game_end(self) -> bool:
        """Kiểm tra và cập nhật nếu ván cờ đã kết thúc."""
        winner = self.board.check_winner()
        if winner is not None:
            self.game_over = True
            if winner == "X":
                self.scores["X"] += 1
                self.lbl_status.configure(text="Bạn đã chiến thắng (X)!", fg="#10b981")
                messagebox.showinfo("Kết quả", "Chúc mừng! Bạn đã thắng.")
            elif winner == "O":
                self.scores["O"] += 1
                self.lbl_status.configure(text="AI đã chiến thắng (O)!", fg="#ef4444")
                messagebox.showinfo("Kết quả", "AI đã chiến thắng. Hãy thử lại!")
            elif winner == "Draw":
                self.scores["Draws"] += 1
                self.lbl_status.configure(text="Trận đấu hòa!", fg="#94a3b8")
                messagebox.showinfo("Kết quả", "Trận đấu hòa!")
            
            self._update_scoreboard()
            return True
        return False

    def _update_status(self):
        """Cập nhật nhãn trạng thái hiển thị lượt đi hiện tại."""
        if self.game_over:
            return
            
        if self.current_turn == "X":
            self.lbl_status.configure(text="Lượt chơi của bạn (X)", fg=self.COLOR_TEXT_LIGHT)
        else:
            algo_name = self.combo_algo.get()
            self.lbl_status.configure(text=f"AI đang suy nghĩ ({algo_name})...", fg="#60a5fa")

    def _update_scoreboard(self):
        """Cập nhật số điểm hiển thị trên bảng điểm."""
        self.lbl_scoreboard.configure(
            text=f"Bạn (X): {self.scores['X']}  |  AI (O): {self.scores['O']}  |  Hòa: {self.scores['Draws']}"
        )
