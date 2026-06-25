# -*- coding: utf-8 -*-
"""
test_ai.py
Tập tin kiểm thử độc lập cho các thuật toán AI (Minimax, Alpha-Beta, Expectimax)
để xác nhận tính chính xác của nước đi và đo lường số lượng trạng thái duyệt.
"""

import sys
import os

# Đảm bảo import được các module trong cùng thư mục
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game_logic import CaroBoard
from minimax import MinimaxAI
from alpha_beta import AlphaBetaAI
from expectimax import ExpectimaxAI

def run_tests():
    print("==================================================")
    print("   BẮT ĐẦU KIỂM THỬ THUẬT TOÁN CARO AI (TIC-TAC-TOE)")
    print("==================================================")
    
    # Khởi tạo bàn cờ 3x3 (Luật thắng 3 quân)
    board = CaroBoard(size=3, to_win=3)
    
    # Thiết lập thế cờ:
    # Hàng 0: [X] [X] [ ]  --> Đối thủ X đang có 2 quân liên tiếp, AI (O) buộc phải chặn ở ô (0, 2)
    # Hàng 1: [ ] [O] [ ]  --> AI đã đi ở tâm (1, 1)
    # Hàng 2: [ ] [ ] [ ]
    board.make_move(0, 0, "X")
    board.make_move(1, 1, "O")
    board.make_move(0, 1, "X")
    
    print("Trạng thái thế cờ thử nghiệm:")
    for r in range(board.size):
        row_str = []
        for c in range(board.size):
            val = board.grid[r][c]
            row_str.append(f"[{val if val else ' '}]")
        print("  ".join(row_str))
    print("-" * 50)
    
    # 1. Kiểm tra Minimax
    mm = MinimaxAI(depth=3)
    best_move_mm = mm.get_best_move(board, "O")
    print(f"1. Minimax (Depth=3):")
    print(f"   - Nước đi tốt nhất AI chọn: {best_move_mm}")
    print(f"   - Số trạng thái đã lượng giá: {mm.nodes_evaluated}")
    
    # 2. Kiểm tra Alpha-Beta Pruning
    ab = AlphaBetaAI(depth=3)
    best_move_ab = ab.get_best_move(board, "O")
    print(f"2. Alpha-Beta Pruning (Depth=3):")
    print(f"   - Nước đi tốt nhất AI chọn: {best_move_ab}")
    print(f"   - Số trạng thái đã lượng giá: {ab.nodes_evaluated}")
    
    # 3. Kiểm tra Expectimax
    ex = ExpectimaxAI(depth=3)
    best_move_ex = ex.get_best_move(board, "O")
    print(f"3. Expectimax (Depth=3):")
    print(f"   - Nước đi tốt nhất AI chọn: {best_move_ex}")
    print(f"   - Số trạng thái đã lượng giá: {ex.nodes_evaluated}")
    
    print("-" * 50)
    # Xác nhận tính đúng đắn (Tất cả phải chặn ở ô (0, 2))
    assert best_move_mm == (0, 2), f"LỖI: Minimax không chặn ở (0, 2) mà trả về {best_move_mm}"
    assert best_move_ab == (0, 2), f"LỖI: Alpha-Beta không chặn ở (0, 2) mà trả về {best_move_ab}"
    assert best_move_ex == (0, 2), f"LỖI: Expectimax không chặn ở (0, 2) mà trả về {best_move_ex}"
    
    print("KẾT QUẢ: Thành công! Cả 3 thuật toán đều phòng thủ chặn nước đi nguy hiểm ở (0, 2).")
    print(f"NHẬN XÉT: Alpha-Beta Pruning duyệt ít trạng thái hơn Minimax ({ab.nodes_evaluated} vs {mm.nodes_evaluated}) nhờ cắt tỉa nhánh hiệu quả!")
    print("==================================================")

if __name__ == "__main__":
    run_tests()
