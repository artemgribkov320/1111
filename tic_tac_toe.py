import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Крестики-нолики")
        self.window.geometry("400x500")
        self.window.configure(bg='#2c3e50')
        
        # Переменные игры
        self.current_player = "X"
        self.board = [""] * 9
        self.game_active = True
        self.player_score = 0
        self.computer_score = 0
        
        # Создание интерфейса
        self.create_widgets()
        
    def create_widgets(self):
        # Заголовок
        title_label = tk.Label(
            self.window,
            text="Крестики-нолики",
            font=("Arial", 24, "bold"),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(pady=20)
        
        # Счет
        self.score_frame = tk.Frame(self.window, bg='#2c3e50')
        self.score_frame.pack(pady=10)
        
        self.player_score_label = tk.Label(
            self.score_frame,
            text=f"Игрок (X): {self.player_score}",
            font=("Arial", 12),
            bg='#2c3e50',
            fg='white'
        )
        self.player_score_label.pack(side=tk.LEFT, padx=20)
        
        self.computer_score_label = tk.Label(
            self.score_frame,
            text=f"Компьютер (O): {self.computer_score}",
            font=("Arial", 12),
            bg='#2c3e50',
            fg='white'
        )
        self.computer_score_label.pack(side=tk.RIGHT, padx=20)
        
        # Игровое поле
        self.game_frame = tk.Frame(self.window, bg='#2c3e50')
        self.game_frame.pack(pady=20)
        
        # Кнопки игрового поля
        self.buttons = []
        for i in range(3):
            for j in range(3):
                button = tk.Button(
                    self.game_frame,
                    text="",
                    font=("Arial", 20, "bold"),
                    width=5,
                    height=2,
                    bg='#34495e',
                    fg='white',
                    command=lambda row=i, col=j: self.button_click(row, col)
                )
                button.grid(row=i, column=j, padx=5, pady=5)
                self.buttons.append(button)
        
        # Кнопка новой игры
        new_game_button = tk.Button(
            self.window,
            text="Новая игра",
            font=("Arial", 14, "bold"),
            bg='#e74c3c',
            fg='white',
            command=self.new_game
        )
        new_game_button.pack(pady=20)
        
        # Статус игры
        self.status_label = tk.Label(
            self.window,
            text="Ваш ход!",
            font=("Arial", 16),
            bg='#2c3e50',
            fg='#27ae60'
        )
        self.status_label.pack(pady=10)
    
    def button_click(self, row, col):
        index = row * 3 + col
        
        if self.board[index] == "" and self.game_active:
            # Ход игрока
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player, bg='#27ae60')
            
            # Проверка победы игрока
            if self.check_winner(self.current_player):
                self.player_score += 1
                self.update_score()
                self.status_label.config(text="Вы победили!", fg='#27ae60')
                self.game_active = False
                messagebox.showinfo("Победа!", "Поздравляем! Вы победили!")
                return
            
            # Проверка ничьей
            if self.check_draw():
                self.status_label.config(text="Ничья!", fg='#f39c12')
                self.game_active = False
                messagebox.showinfo("Ничья!", "Игра закончилась вничью!")
                return
            
            # Ход компьютера
            self.current_player = "O"
            self.status_label.config(text="Ход компьютера...", fg='#e74c3c')
            self.window.after(500, self.computer_move)
    
    def computer_move(self):
        if not self.game_active:
            return
            
        # Простой ИИ: случайный ход
        empty_cells = [i for i, cell in enumerate(self.board) if cell == ""]
        if empty_cells:
            move = random.choice(empty_cells)
            self.board[move] = "O"
            self.buttons[move].config(text="O", bg='#e74c3c')
            
            # Проверка победы компьютера
            if self.check_winner("O"):
                self.computer_score += 1
                self.update_score()
                self.status_label.config(text="Компьютер победил!", fg='#e74c3c')
                self.game_active = False
                messagebox.showinfo("Поражение!", "Компьютер победил!")
                return
            
            # Проверка ничьей
            if self.check_draw():
                self.status_label.config(text="Ничья!", fg='#f39c12')
                self.game_active = False
                messagebox.showinfo("Ничья!", "Игра закончилась вничью!")
                return
            
            # Возврат хода игроку
            self.current_player = "X"
            self.status_label.config(text="Ваш ход!", fg='#27ae60')
    
    def check_winner(self, player):
        # Выигрышные комбинации
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Горизонтали
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Вертикали
            [0, 4, 8], [2, 4, 6]              # Диагонали
        ]
        
        for combo in win_combinations:
            if (self.board[combo[0]] == player and 
                self.board[combo[1]] == player and 
                self.board[combo[2]] == player):
                return True
        return False
    
    def check_draw(self):
        return "" not in self.board
    
    def update_score(self):
        self.player_score_label.config(text=f"Игрок (X): {self.player_score}")
        self.computer_score_label.config(text=f"Компьютер (O): {self.computer_score}")
    
    def new_game(self):
        # Сброс игры
        self.board = [""] * 9
        self.current_player = "X"
        self.game_active = True
        
        # Очистка кнопок
        for button in self.buttons:
            button.config(text="", bg='#34495e')
        
        # Обновление статуса
        self.status_label.config(text="Ваш ход!", fg='#27ae60')
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = TicTacToe()
    game.run()