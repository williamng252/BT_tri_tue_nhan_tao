# -*- coding: utf-8 -*-
"""
main.py
Điểm khởi chạy chương trình chính cho trò chơi Caro AI.
"""

import tkinter as tk
from ui import CaroGUI

def main():
    # Khởi tạo cửa sổ chính Tkinter
    root = tk.Tk()
    
    # Khởi tạo giao diện ứng dụng Caro
    app = CaroGUI(root)
    
    # Bắt đầu vòng lặp sự kiện của giao diện
    root.mainloop()

if __name__ == "__main__":
    main()
