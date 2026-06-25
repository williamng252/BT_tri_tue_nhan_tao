# -*- coding: utf-8 -*-
"""
minimax.py
Triển khai thuật toán tìm kiếm Minimax cơ bản cho AI chơi Caro.
"""

import math
from typing import Tuple, Optional
from game_logic import CaroBoard

class MinimaxAI:
    def __init__(self, depth: int = 3):
        self.depth = depth
        self.nodes_evaluated = 0  # Theo dõi số trạng thái đã lượng giá

    def get_best_move(self, board: CaroBoard, ai_player: str) -> Optional[Tuple[int, int]]:
        """
        Tìm nước đi tốt nhất cho AI sử dụng thuật toán Minimax.
        """
        self.nodes_evaluated = 0
        _, best_move = self._minimax(board, self.depth, True, ai_player)
        return best_move

    def _minimax(self, board: CaroBoard, depth: int, is_maximizing: bool, ai_player: str) -> Tuple[float, Optional[Tuple[int, int]]]:
        # 1. Kiểm tra trạng thái dừng (Thắng / Thua / Hòa)
        winner = board.check_winner()
        opponent = "O" if ai_player == "X" else "X"

        if winner == ai_player:
            # Ưu tiên thắng nhanh hơn (cộng thêm depth để khuyến khích đường đi ngắn hơn)
            return 1000000 + depth, None
        elif winner == opponent:
            # Ưu tiên thua muộn hơn (trừ depth)
            return -1000000 - depth, None
        elif winner == "Draw":
            return 0, None

        # Nếu đạt độ sâu tối đa, trả về điểm số lượng giá của bàn cờ hiện tại
        if depth == 0:
            self.nodes_evaluated += 1
            return board.evaluate(ai_player), None

        # Lấy danh sách nước đi tiềm năng (đã được lọc để tăng tốc)
        relevant_moves = board.get_relevant_moves()
        if not relevant_moves:
            return 0, None

        best_move = None

        if is_maximizing:
            max_eval = -math.inf
            for r, c in relevant_moves:
                # Thử đi nước này
                board.make_move(r, c, ai_player)
                eval_val, _ = self._minimax(board, depth - 1, False, ai_player)
                # Quay lui (backtrack) để trả lại bàn cờ gốc
                board.undo_move(r, c)

                if eval_val > max_eval:
                    max_eval = eval_val
                    best_move = (r, c)
            return max_eval, best_move
        else:
            min_eval = math.inf
            for r, c in relevant_moves:
                # Giả định đối thủ đi nước này
                board.make_move(r, c, opponent)
                eval_val, _ = self._minimax(board, depth - 1, True, ai_player)
                # Quay lui (backtrack)
                board.undo_move(r, c)

                if eval_val < min_eval:
                    min_eval = eval_val
                    best_move = (r, c)
            return min_eval, best_move
