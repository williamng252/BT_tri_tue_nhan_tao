# -*- coding: utf-8 -*-
"""
game_logic.py
Chứa các class và hàm xử lý logic cốt lõi của trò chơi Caro / Tic-Tac-Toe.
Bao gồm: trạng thái bàn cờ, kiểm tra thắng thua, lượng giá heuristic và lọc nước đi tiềm năng.
"""

from typing import List, Tuple, Optional, Set

class CaroBoard:
    def __init__(self, size: int = 10, to_win: int = 5):
        self.size = size
        self.to_win = to_win
        # Khởi tạo bàn cờ rỗng (None đại diện cho ô trống)
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        # Theo dõi số ô đã đánh để kiểm tra hòa nhanh
        self.moves_count = 0

    def copy(self) -> 'CaroBoard':
        """Tạo một bản sao sâu của bàn cờ hiện tại."""
        new_board = CaroBoard(self.size, self.to_win)
        new_board.grid = [row[:] for row in self.grid]
        new_board.moves_count = self.moves_count
        return new_board

    def make_move(self, row: int, col: int, player: str) -> bool:
        """Thực hiện một nước đi của người chơi ('X' hoặc 'O')."""
        if 0 <= row < self.size and 0 <= col < self.size and self.grid[row][col] is None:
            self.grid[row][col] = player
            self.moves_count += 1
            return True
        return False

    def undo_move(self, row: int, col: int):
        """Hủy nước đi tại vị trí chỉ định (thuận tiện cho backtracking trong AI)."""
        if 0 <= row < self.size and 0 <= col < self.size and self.grid[row][col] is not None:
            self.grid[row][col] = None
            self.moves_count -= 1

    def is_full(self) -> bool:
        """Kiểm tra bàn cờ đã đầy chưa."""
        return self.moves_count >= self.size * self.size

    def check_winner(self) -> Optional[str]:
        """
        Kiểm tra xem có người chiến thắng chưa.
        Trả về 'X', 'O' nếu thắng, 'Draw' nếu hòa, hoặc None nếu game chưa kết thúc.
        """
        # Quét toàn bộ bàn cờ để tìm chuỗi thắng
        for r in range(self.size):
            for c in range(self.size):
                player = self.grid[r][c]
                if player is None:
                    continue

                # Kiểm tra 4 hướng: ngang, dọc, chéo xuôi, chéo ngược
                directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
                for dr, dc in directions:
                    count = 1
                    # Đi về phía trước
                    nr, nc = r + dr, c + dc
                    while 0 <= nr < self.size and 0 <= nc < self.size and self.grid[nr][nc] == player:
                        count += 1
                        if count == self.to_win:
                            return player
                        nr += dr
                        nc += dc

        if self.is_full():
            return "Draw"

        return None

    def get_relevant_moves(self) -> List[Tuple[int, int]]:
        """
        Lọc các nước đi tiềm năng: chỉ chọn những ô trống nằm trong phạm vi 1 hoặc 2 ô
        xung quanh các quân cờ đã đánh. Điều này giúp giảm đáng kể branching factor.
        """
        relevant_moves: Set[Tuple[int, int]] = set()
        has_stones = False

        # Quét bàn cờ tìm các quân cờ đã đánh
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] is not None:
                    has_stones = True
                    # Thêm các ô trống trong khoảng cách ranh giới 1-2 ô xung quanh quân này
                    for dr in range(-2, 3):
                        for dc in range(-2, 3):
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < self.size and 0 <= nc < self.size:
                                if self.grid[nr][nc] is None:
                                    relevant_moves.add((nr, nc))

        if not has_stones:
            # Nếu bàn cờ trống rỗng hoàn toàn, chỉ trả về ô trung tâm bàn cờ
            center = self.size // 2
            return [(center, center)]

        return list(relevant_moves)

    def evaluate(self, ai_player: str) -> int:
        """
        Hàm lượng giá trạng thái bàn cờ hiện tại đối với người chơi `ai_player`.
        Điểm số cao có lợi cho AI, thấp có lợi cho đối thủ.
        """
        opponent = "O" if ai_player == "X" else "X"
        total_score = 0
        w = self.to_win

        # Hàm tính điểm cho một dãy (window) gồm w quân cờ liên tiếp
        def score_window(window: List[Optional[str]]) -> int:
            ai_count = window.count(ai_player)
            opp_count = window.count(opponent)
            
            # Nếu cả 2 đều có quân trong cửa sổ này, cửa sổ này vô giá trị
            if ai_count > 0 and opp_count > 0:
                return 0
                
            if ai_count > 0:
                if ai_count == w:
                    return 100000
                elif ai_count == w - 1:
                    return 5000
                elif ai_count == w - 2:
                    return 500
                elif ai_count == w - 3:
                    return 50
                elif ai_count == 1:
                    return 2
            elif opp_count > 0:
                if opp_count == w:
                    return -100000
                elif opp_count == w - 1:
                    return -10000  # Ưu tiên chặn đối thủ trước khi tự tạo thế
                elif opp_count == w - 2:
                    return -1000
                elif opp_count == w - 3:
                    return -100
                elif opp_count == 1:
                    return -2
            return 0

        # 1. Quét theo hàng ngang
        for r in range(self.size):
            for c in range(self.size - w + 1):
                window = [self.grid[r][c + i] for i in range(w)]
                total_score += score_window(window)

        # 2. Quét theo cột dọc
        for c in range(self.size):
            for r in range(self.size - w + 1):
                window = [self.grid[r + i][c] for i in range(w)]
                total_score += score_window(window)

        # 3. Quét chéo xuôi (từ trái qua phải, trên xuống dưới)
        for r in range(self.size - w + 1):
            for c in range(self.size - w + 1):
                window = [self.grid[r + i][c + i] for i in range(w)]
                total_score += score_window(window)

        # 4. Quét chéo ngược (từ phải qua trái, trên xuống dưới)
        for r in range(self.size - w + 1):
            for c in range(w - 1, self.size):
                window = [self.grid[r + i][c - i] for i in range(w)]
                total_score += score_window(window)

        return total_score
