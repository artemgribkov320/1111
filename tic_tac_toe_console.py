import random
import os

class ConsoleTicTacToe:
    def __init__(self):
        self.board = [" " for _ in range(9)]
        self.current_player = "X"
        self.game_active = True
        self.player_score = 0
        self.computer_score = 0
        
    def clear_screen(self):
        """Очистка экрана"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_board(self):
        """Вывод игрового поля"""
        print("\n" + "="*30)
        print("         КРЕСТИКИ-НОЛИКИ")
        print("="*30)
        print(f"Счет: Игрок (X) - {self.player_score} | Компьютер (O) - {self.computer_score}")
        print("="*30)
        print()
        
        for i in range(0, 9, 3):
            print(f" {self.board[i]} | {self.board[i+1]} | {self.board[i+2]} ")
            if i < 6:
                print("-----------")
        print()
        print("Позиции: 0-8 (слева направо, сверху вниз)")
        print("="*30)
    
    def is_valid_move(self, position):
        """Проверка валидности хода"""
        return 0 <= position <= 8 and self.board[position] == " "
    
    def make_move(self, position, player):
        """Сделать ход"""
        self.board[position] = player
    
    def check_winner(self, player):
        """Проверка победы"""
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
        """Проверка ничьей"""
        return " " not in self.board
    
    def get_available_moves(self):
        """Получить доступные ходы"""
        return [i for i, cell in enumerate(self.board) if cell == " "]
    
    def computer_move_easy(self):
        """Простой ИИ - случайный ход"""
        available_moves = self.get_available_moves()
        if available_moves:
            return random.choice(available_moves)
        return None
    
    def computer_move_medium(self):
        """Средний ИИ - пытается выиграть и блокировать"""
        # Попытка выиграть
        for move in self.get_available_moves():
            self.board[move] = "O"
            if self.check_winner("O"):
                self.board[move] = " "
                return move
            self.board[move] = " "
        
        # Блокировка игрока
        for move in self.get_available_moves():
            self.board[move] = "X"
            if self.check_winner("X"):
                self.board[move] = " "
                return move
            self.board[move] = " "
        
        # Случайный ход
        return self.computer_move_easy()
    
    def computer_move_hard(self):
        """Сложный ИИ - минимакс алгоритм"""
        best_score = float('-inf')
        best_move = None
        
        for move in self.get_available_moves():
            self.board[move] = "O"
            score = self.minimax(self.board, 0, False)
            self.board[move] = " "
            
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move
    
    def minimax(self, board, depth, is_maximizing):
        """Минимакс алгоритм"""
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
                if cell == " ":
                    board[i] = "O"
                    score = self.minimax(board, depth + 1, False)
                    board[i] = " "
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i, cell in enumerate(board):
                if cell == " ":
                    board[i] = "X"
                    score = self.minimax(board, depth + 1, True)
                    board[i] = " "
                    best_score = min(score, best_score)
            return best_score
    
    def get_difficulty(self):
        """Выбор сложности ИИ"""
        while True:
            print("\nВыберите сложность компьютера:")
            print("1 - Легкий (случайные ходы)")
            print("2 - Средний (пытается выиграть и блокировать)")
            print("3 - Сложный (непобедимый)")
            
            try:
                choice = int(input("Ваш выбор (1-3): "))
                if choice in [1, 2, 3]:
                    return choice
                else:
                    print("Пожалуйста, выберите 1, 2 или 3.")
            except ValueError:
                print("Пожалуйста, введите число.")
    
    def player_move(self):
        """Ход игрока"""
        while True:
            try:
                position = int(input(f"Ваш ход (0-8): "))
                if self.is_valid_move(position):
                    return position
                else:
                    print("Неверная позиция! Попробуйте снова.")
            except ValueError:
                print("Пожалуйста, введите число от 0 до 8.")
    
    def computer_move(self, difficulty):
        """Ход компьютера"""
        print("Компьютер думает...")
        
        if difficulty == 1:
            move = self.computer_move_easy()
        elif difficulty == 2:
            move = self.computer_move_medium()
        else:
            move = self.computer_move_hard()
        
        if move is not None:
            self.make_move(move, "O")
            print(f"Компьютер выбрал позицию {move}")
    
    def play_game(self):
        """Основной игровой цикл"""
        print("Добро пожаловать в Крестики-нолики!")
        difficulty = self.get_difficulty()
        
        while True:
            self.clear_screen()
            self.print_board()
            
            if self.current_player == "X":
                # Ход игрока
                position = self.player_move()
                self.make_move(position, "X")
                
                # Проверка победы игрока
                if self.check_winner("X"):
                    self.player_score += 1
                    self.clear_screen()
                    self.print_board()
                    print("🎉 Поздравляем! Вы победили! 🎉")
                    break
                
                # Проверка ничьей
                if self.check_draw():
                    self.clear_screen()
                    self.print_board()
                    print("🤝 Ничья! 🤝")
                    break
                
                self.current_player = "O"
                
            else:
                # Ход компьютера
                self.computer_move(difficulty)
                
                # Проверка победы компьютера
                if self.check_winner("O"):
                    self.computer_score += 1
                    self.clear_screen()
                    self.print_board()
                    print("💻 Компьютер победил! 💻")
                    break
                
                # Проверка ничьей
                if self.check_draw():
                    self.clear_screen()
                    self.print_board()
                    print("🤝 Ничья! 🤝")
                    break
                
                self.current_player = "X"
    
    def play_again(self):
        """Спросить о новой игре"""
        while True:
            choice = input("\nХотите сыграть еще раз? (да/нет): ").lower()
            if choice in ['да', 'д', 'yes', 'y']:
                return True
            elif choice in ['нет', 'н', 'no', 'n']:
                return False
            else:
                print("Пожалуйста, ответьте 'да' или 'нет'.")
    
    def run(self):
        """Запуск игры"""
        while True:
            # Сброс игры
            self.board = [" " for _ in range(9)]
            self.current_player = "X"
            self.game_active = True
            
            self.play_game()
            
            if not self.play_again():
                print("\nСпасибо за игру! До свидания! 👋")
                break

if __name__ == "__main__":
    game = ConsoleTicTacToe()
    game.run()