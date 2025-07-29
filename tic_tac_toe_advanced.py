import tkinter as tk
from tkinter import messagebox, ttk
import random

class AdvancedTicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Крестики-нолики - Продвинутая версия")
        self.window.geometry("500x600")
        self.window.configure(bg='#2c3e50')
        
        # Переменные игры
        self.current_player = "X"
        self.board = [""] * 9
        self.game_active = True
        self.player1_score = 0
        self.player2_score = 0
        self.game_mode = "computer"  # "computer" или "two_players"
        self.ai_difficulty = "medium"  # "easy", "medium", "hard"
        
        # Создание интерфейса
        self.create_widgets()
        
    def create_widgets(self):
        # Заголовок
        title_label = tk.Label(
            self.window,
            text="Крестики-нолики",
            font=("Arial", 28, "bold"),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(pady=20)
        
        # Настройки игры
        settings_frame = tk.Frame(self.window, bg='#2c3e50')
        settings_frame.pack(pady=10)
        
        # Выбор режима игры
        mode_label = tk.Label(
            settings_frame,
            text="Режим игры:",
            font=("Arial", 12),
            bg='#2c3e50',
            fg='white'
        )
        mode_label.pack()
        
        self.mode_var = tk.StringVar(value="computer")
        mode_combo = ttk.Combobox(
            settings_frame,
            textvariable=self.mode_var,
            values=["Игра против компьютера", "Игра для двух игроков"],
            state="readonly",
            width=25
        )
        mode_combo.pack(pady=5)
        mode_combo.bind("<<ComboboxSelected>>", self.on_mode_change)
        
        # Выбор сложности ИИ
        self.ai_frame = tk.Frame(settings_frame, bg='#2c3e50')
        self.ai_frame.pack(pady=5)
        
        ai_label = tk.Label(
            self.ai_frame,
            text="Сложность ИИ:",
            font=("Arial", 12),
            bg='#2c3e50',
            fg='white'
        )
        ai_label.pack()
        
        self.ai_var = tk.StringVar(value="medium")
        ai_combo = ttk.Combobox(
            self.ai_frame,
            textvariable=self.ai_var,
            values=["Легкий", "Средний", "Сложный"],
            state="readonly",
            width=15
        )
        ai_combo.pack(pady=5)
        ai_combo.bind("<<ComboboxSelected>>", self.on_ai_change)
        
        # Счет
        self.score_frame = tk.Frame(self.window, bg='#2c3e50')
        self.score_frame.pack(pady=10)
        
        self.player1_score_label = tk.Label(
            self.score_frame,
            text="Игрок 1 (X): 0",
            font=("Arial", 12),
            bg='#2c3e50',
            fg='#27ae60'
        )
        self.player1_score_label.pack(side=tk.LEFT, padx=20)
        
        self.player2_score_label = tk.Label(
            self.score_frame,
            text="Игрок 2 (O): 0",
            font=("Arial", 12),
            bg='#2c3e50',
            fg='#e74c3c'
        )
        self.player2_score_label.pack(side=tk.RIGHT, padx=20)
        
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
                    font=("Arial", 24, "bold"),
                    width=4,
                    height=2,
                    bg='#34495e',
                    fg='white',
                    command=lambda row=i, col=j: self.button_click(row, col)
                )
                button.grid(row=i, column=j, padx=3, pady=3)
                self.buttons.append(button)
        
        # Кнопки управления
        control_frame = tk.Frame(self.window, bg='#2c3e50')
        control_frame.pack(pady=20)
        
        new_game_button = tk.Button(
            control_frame,
            text="Новая игра",
            font=("Arial", 14, "bold"),
            bg='#e74c3c',
            fg='white',
            command=self.new_game
        )
        new_game_button.pack(side=tk.LEFT, padx=10)
        
        reset_score_button = tk.Button(
            control_frame,
            text="Сбросить счет",
            font=("Arial", 14, "bold"),
            bg='#f39c12',
            fg='white',
            command=self.reset_score
        )
        reset_score_button.pack(side=tk.RIGHT, padx=10)
        
        # Статус игры
        self.status_label = tk.Label(
            self.window,
            text="Ваш ход!",
            font=("Arial", 16, "bold"),
            bg='#2c3e50',
            fg='#27ae60'
        )
        self.status_label.pack(pady=10)
    
    def on_mode_change(self, event):
        mode_map = {
            "Игра против компьютера": "computer",
            "Игра для двух игроков": "two_players"
        }
        self.game_mode = mode_map[self.mode_var.get()]
        self.new_game()
    
    def on_ai_change(self, event):
        difficulty_map = {
            "Легкий": "easy",
            "Средний": "medium", 
            "Сложный": "hard"
        }
        self.ai_difficulty = difficulty_map[self.ai_var.get()]
    
    def button_click(self, row, col):
        index = row * 3 + col
        
        if self.board[index] == "" and self.game_active:
            # Ход игрока
            self.board[index] = self.current_player
            color = '#27ae60' if self.current_player == "X" else '#e74c3c'
            self.buttons[index].config(text=self.current_player, bg=color)
            
            # Проверка победы
            if self.check_winner(self.current_player):
                if self.current_player == "X":
                    self.player1_score += 1
                else:
                    self.player2_score += 1
                self.update_score()
                winner_text = "Игрок 1 победил!" if self.current_player == "X" else "Игрок 2 победил!"
                self.status_label.config(text=winner_text, fg=color)
                self.game_active = False
                messagebox.showinfo("Победа!", f"Поздравляем! {winner_text}")
                return
            
            # Проверка ничьей
            if self.check_draw():
                self.status_label.config(text="Ничья!", fg='#f39c12')
                self.game_active = False
                messagebox.showinfo("Ничья!", "Игра закончилась вничью!")
                return
            
            # Смена игрока
            self.current_player = "O" if self.current_player == "X" else "X"
            
            # Если игра против компьютера и ход компьютера
            if self.game_mode == "computer" and self.current_player == "O":
                self.status_label.config(text="Ход компьютера...", fg='#e74c3c')
                self.window.after(500, self.computer_move)
            else:
                player_text = "Игрок 1" if self.current_player == "X" else "Игрок 2"
                self.status_label.config(text=f"Ход {player_text}!", fg=color)
    
    def computer_move(self):
        if not self.game_active:
            return
            
        if self.ai_difficulty == "easy":
            move = self.get_random_move()
        elif self.ai_difficulty == "medium":
            move = self.get_medium_move()
        else:  # hard
            move = self.get_best_move()
        
        if move is not None:
            self.board[move] = "O"
            self.buttons[move].config(text="O", bg='#e74c3c')
            
            # Проверка победы компьютера
            if self.check_winner("O"):
                self.player2_score += 1
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
    
    def get_random_move(self):
        empty_cells = [i for i, cell in enumerate(self.board) if cell == ""]
        return random.choice(empty_cells) if empty_cells else None
    
    def get_medium_move(self):
        # Сначала попробуем выиграть
        for i, cell in enumerate(self.board):
            if cell == "":
                self.board[i] = "O"
                if self.check_winner("O"):
                    self.board[i] = ""
                    return i
                self.board[i] = ""
        
        # Затем заблокируем ход игрока
        for i, cell in enumerate(self.board):
            if cell == "":
                self.board[i] = "X"
                if self.check_winner("X"):
                    self.board[i] = ""
                    return i
                self.board[i] = ""
        
        # Иначе случайный ход
        return self.get_random_move()
    
    def get_best_move(self):
        # Минимакс алгоритм для идеальной игры
        best_score = float('-inf')
        best_move = None
        
        for i, cell in enumerate(self.board):
            if cell == "":
                self.board[i] = "O"
                score = self.minimax(self.board, 0, False)
                self.board[i] = ""
                
                if score > best_score:
                    best_score = score
                    best_move = i
        
        return best_move
    
    def minimax(self, board, depth, is_maximizing):
        # Проверка терминальных состояний
        if self.check_winner("O"):
            return 1
        if self.check_winner("X"):
            return -1
        if self.check_draw():
            return 0
        
        if is_maximizing:
            best_score = float('-inf')
            for i, cell in enumerate(board):
                if cell == "":
                    board[i] = "O"
                    score = self.minimax(board, depth + 1, False)
                    board[i] = ""
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i, cell in enumerate(board):
                if cell == "":
                    board[i] = "X"
                    score = self.minimax(board, depth + 1, True)
                    board[i] = ""
                    best_score = min(score, best_score)
            return best_score
    
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
        self.player1_score_label.config(text=f"Игрок 1 (X): {self.player1_score}")
        self.player2_score_label.config(text=f"Игрок 2 (O): {self.player2_score}")
    
    def new_game(self):
        # Сброс игры
        self.board = [""] * 9
        self.current_player = "X"
        self.game_active = True
        
        # Очистка кнопок
        for button in self.buttons:
            button.config(text="", bg='#34495e')
        
        # Обновление статуса
        if self.game_mode == "computer":
            self.status_label.config(text="Ваш ход!", fg='#27ae60')
        else:
            self.status_label.config(text="Ход Игрока 1!", fg='#27ae60')
    
    def reset_score(self):
        self.player1_score = 0
        self.player2_score = 0
        self.update_score()
        self.new_game()
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = AdvancedTicTacToe()
    game.run()