import random
import time
from typing import List

class VacuumRobot:
    def __init__(self, grid: List[List[int]], start_x: int, start_y: int):
        self.grid = grid
        self.m = len(grid)       # Số hàng (x)
        self.n = len(grid[0])    # Số cột (y)
        self.x = start_x
        self.y = start_y
        self.steps = 0           # Đếm số bước đã đi

    def print_state(self, action_msg: str = ""):
        print(f"--- BƯỚC {self.steps}: {action_msg} ---")
        for i in range(self.m):
            row_display = []
            for j in range(self.n):
                if i == self.x and j == self.y:
                    # Đánh dấu vị trí Robot bằng ngoặc vuông [ ]
                    row_display.append(f"[{self.grid[i][j]}]")
                elif self.grid[i][j] == 2:
                    # Hiển thị vật cản bằng chữ X cho dễ nhìn
                    row_display.append(" X ")
                else:
                    row_display.append(f" {self.grid[i][j]} ")
            print("  ".join(row_display))
        print("-" * 30)

    def possible_move(self) -> List[str]:
        """
        Tập luật 1 (Nâng cấp): Xác định hướng đi hợp lệ.
        Điều kiện: Không đâm vào tường mép VÀ không đâm vào vật cản (giá trị = 2).
        """
        moves = []
        # Kiểm tra lên trên: Không sát mép trên VÀ ô phía trên không phải là 2
        if self.x > 0 and self.grid[self.x - 1][self.y] != 2:
            moves.append("up")
            
        # Kiểm tra xuống dưới
        if self.x < self.m - 1 and self.grid[self.x + 1][self.y] != 2:
            moves.append("down")
            
        # Kiểm tra sang trái
        if self.y > 0 and self.grid[self.x][self.y - 1] != 2:
            moves.append("left")
            
        # Kiểm tra sang phải
        if self.y < self.n - 1 and self.grid[self.x][self.y + 1] != 2:
            moves.append("right")
            
        return moves

    def is_all_clean(self) -> bool:
        """Kiểm tra xem toàn bộ phòng đã sạch bụi (số 1) chưa."""
        for row in self.grid:
            if 1 in row:
                return False
        return True

    def run(self, max_steps: int = 50):
        """Vận hành vòng lặp của máy hút bụi."""
        print("=== TRẠNG THÁI BAN ĐẦU ===")
        self.print_state("Robot khởi động")

        while self.steps < max_steps:
            if self.is_all_clean():
                print(f"THÀNH CÔNG: Đã dọn sạch toàn bộ bụi sau {self.steps} bước!")
                break

            self.steps += 1
            time.sleep(0.5)  

            current_value = self.grid[self.x][self.y]
            valid_moves = self.possible_move()
            action_log = ""

            # Xử lý trường hợp Robot bị kẹt kín bởi vật cản (không có đường lui)
            if not valid_moves:
                print("THẤT BẠI: Robot bị kẹt cứng giữa các vật cản và không thể di chuyển!")
                break

            # --- Tập luật 2: Quyết định hành động ---
            if current_value == 1:
                # Nếu có bụi -> Hút bụi (chuyển 1 thành 0)
                self.grid[self.x][self.y] = 0
                action_log += "HÚT BỤI và "

            # Chọn ngẫu nhiên hướng đi an toàn
            next_move = random.choice(valid_moves)
            action_log += f"Đi '{next_move.upper()}'"

            self.print_state(action_log)

            # --- Cập nhật vị trí mới ---cd BT_tri_tue_nhan_tao
            if next_move == "up":
                self.x -= 1
            elif next_move == "down":
                self.x += 1
            elif next_move == "left":
                self.y -= 1
            elif next_move == "right":
                self.y += 1
                
        else:
            print(f"CẢNH BÁO: Đã đạt giới hạn {max_steps} bước nhưng chưa dọn xong.")

if __name__ == "__main__":
    # Khởi tạo bản đồ 4x4 để có không gian di chuyển rộng hơn
    # 1: Có bụi, 0: Sạch, 2: Vật cản
    room_grid = [
        [0, 1, 0, 2],
        [0, 2, 0, 1],
        [0, 2, 1, 0],
        [1, 0, 0, 0]
    ]

    # Đặt robot ở tọa độ góc trên cùng bên trái (x=0, y=0)
    agent = VacuumRobot(grid=room_grid, start_x=0, start_y=0)
    
    # Bắt đầu dọn dẹp với giới hạn số bước lớn hơn một chút
    agent.run(max_steps=50)