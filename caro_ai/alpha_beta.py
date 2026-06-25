# -*- coding: utf-8 -*-
"""
alpha_beta.py
Triển khai thuật toán Alpha-Beta Pruning (Cắt tỉa Alpha-Beta) cho AI chơi Caro.
Có tích hợp sắp xếp nước đi (Move Ordering) để tối ưu hóa hiệu suất cắt tỉa.
"""

import math
from typing import Tuple, Optional
from game_logic import CaroBoard

class AlphaBetaAI:
    def __init__(self, depth: int = 3):
        self.depth = depth
        self.nodes_evaluated = 0  # Theo dõi số trạng thái đã lượng giá

    def get_best_move(self, board: CaroBoard, ai_player: str) -> Optional[Tuple[int, int]]:
        """
        Tìm nước đi tốt nhất sử dụng thuật toán cắt tỉa Alpha-Beta.
        """
        self.nodes_evaluated = 0
        _, best_move = self._alphabeta(board, self.depth, -math.inf, math.inf, True, ai_player)
        return best_move

    def _alphabeta(self, board: CaroBoard, depth: int, alpha: float, beta: float, is_maximizing: bool, ai_player: str) -> Tuple[float, Optional[Tuple[int, int]]]:
        # 1. Kiểm tra trạng thái dừng (Thắng / Thua / Hòa)
        winner = board.check_winner()
        opponent = "O" if ai_player == "X" else "X"

        if winner == ai_player:
            return 1000000 + depth, None
        elif winner == opponent:
            return -1000000 - depth, None
        elif winner == "Draw":
            return 0, None

        # Đạt độ sâu tối đa
        if depth == 0:
            self.nodes_evaluated += 1
            return board.evaluate(ai_player), None

        relevant_moves = board.get_relevant_moves()
        if not relevant_moves:
            return 0, None

        # --- Tối ưu hóa: Move Ordering (Sắp xếp nước đi) ---
        # Sắp xếp các nước đi có triển vọng trước để tối đa hóa khả năng cắt tỉa của Alpha-Beta.
        move_scores = []
        for r, c in relevant_moves:
            # Thử lượng giá nhanh từng nước đi riêng lẻ
            board.make_move(r, c, ai_player if is_maximizing else opponent)
            score = board.evaluate(ai_player)
            board.undo_move(r, c)
            move_scores.append((score, (r, c)))

        # Sắp xếp giảm dần nếu đang cực đại hóa (AI), tăng dần nếu đang cực tiểu hóa (Đối thủ)
        move_scores.sort(key=lambda x: x[0], reverse=is_maximizing)
        sorted_moves = [move for _, move in move_scores]

        best_move = None

        if is_maximizing:
            max_eval = -math.inf
            for r, c in sorted_moves:
                board.make_move(r, c, ai_player)
                eval_val, _ = self._alphabeta(board, depth - 1, alpha, beta, False, ai_player)
                board.undo_move(r, c)

                if eval_val > max_eval:
                    max_eval = eval_val
                    best_move = (r, c)
                
                alpha = max(alpha, eval_val)
                if beta <= alpha:
                    break  # Cắt tỉa Beta (không cần duyệt các nhánh còn lại)
            return max_eval, best_move
        else:
            min_eval = math.inf
            for r, c in sorted_moves:
                board.make_move(r, c, opponent)
                eval_val, _ = self._alphabeta(board, depth - 1, alpha, beta, True, ai_player)
                board.undo_move(r, c)

                if eval_val < min_eval:
                    min_eval = eval_val
                    best_move = (r, c)

                beta = min(beta, eval_val)
                if beta <= alpha:
                    break  # Cắt tỉa Alpha
            return min_eval, best_move
