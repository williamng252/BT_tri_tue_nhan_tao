# -*- coding: utf-8 -*-
"""
expectimax.py
Triển khai thuật toán Expectimax cho AI chơi Caro.
Mô hình hóa lượt đi của đối thủ (Chance Node) bằng cách phân bổ xác suất cho các nước đi tốt nhất.
"""

import math
from typing import Tuple, Optional, List
from game_logic import CaroBoard

class ExpectimaxAI:
    def __init__(self, depth: int = 3):
        self.depth = depth
        self.nodes_evaluated = 0  # Theo dõi số trạng thái đã lượng giá

    def get_best_move(self, board: CaroBoard, ai_player: str) -> Optional[Tuple[int, int]]:
        """
        Tìm nước đi tốt nhất sử dụng thuật toán Expectimax.
        """
        self.nodes_evaluated = 0
        _, best_move = self._expectimax(board, self.depth, True, ai_player)
        return best_move

    def _expectimax(self, board: CaroBoard, depth: int, is_maximizing: bool, ai_player: str) -> Tuple[float, Optional[Tuple[int, int]]]:
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

        best_move = None

        if is_maximizing:
            # Lượt của AI: Cực đại hóa điểm số kỳ vọng
            max_eval = -math.inf
            for r, c in relevant_moves:
                board.make_move(r, c, ai_player)
                eval_val, _ = self._expectimax(board, depth - 1, False, ai_player)
                board.undo_move(r, c)

                if eval_val > max_eval:
                    max_eval = eval_val
                    best_move = (r, c)
            return max_eval, best_move
        else:
            # Lượt của đối thủ (Chance Node): Tính giá trị trung bình có trọng số (kỳ vọng)
            # Chúng ta giả định đối thủ sẽ chọn các nước đi tốt nhất với xác suất cao hơn.
            move_scores = []
            for r, c in relevant_moves:
                board.make_move(r, c, opponent)
                # Đánh giá dưới góc nhìn của đối thủ
                score = board.evaluate(opponent)
                board.undo_move(r, c)
                move_scores.append((score, (r, c)))

            # Sắp xếp các nước đi tốt nhất của đối thủ (giảm dần theo điểm đối thủ)
            move_scores.sort(key=lambda x: x[0], reverse=True)

            # Mô hình hóa xác suất lựa chọn của đối thủ:
            # - Nước đi tốt nhất (Best Move): 70% cơ hội chọn
            # - Nước đi tốt thứ 2: 15%
            # - Nước đi tốt thứ 3: 10%
            # - Nước đi tốt thứ 4: 5%
            p_distribution = [0.70, 0.15, 0.10, 0.05]
            num_moves = len(move_scores)
            
            n_choices = min(len(p_distribution), num_moves)
            selected_moves = move_scores[:n_choices]
            
            # Chuẩn hóa lại xác suất nếu số nước đi thực tế nhỏ hơn 4
            weights = p_distribution[:n_choices]
            total_weight = sum(weights)
            probabilities = [w / total_weight for w in weights]

            expected_value = 0.0

            # Tính tổng kỳ vọng
            for i, (score, (r, c)) in enumerate(selected_moves):
                board.make_move(r, c, opponent)
                eval_val, _ = self._expectimax(board, depth - 1, True, ai_player)
                board.undo_move(r, c)
                
                expected_value += eval_val * probabilities[i]

            # Trả về giá trị kỳ vọng và nước đi tốt nhất của đối thủ (nước đi đại diện)
            best_move = selected_moves[0][1] if selected_moves else None
            return expected_value, best_move
