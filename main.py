import pygame
import sys

# Розміри вікна гри
WIDTH = 300
HEIGHT = 300

# Колір клітинок
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Розміри клітинки
CELL_SIZE = WIDTH // 3

# Ініціалізація Pygame
pygame.init()

# Створення вікна гри
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

# Ініціалізація гри "хрестики-нулики"
game_board = [[None, None, None], [None, None, None], [None, None, None]]
current_player = "X"
game_over = False

# Оновлення екрану
def update_screen():
    screen.fill(WHITE)

    # Малюємо лінії
    pygame.draw.line(screen, BLACK, (CELL_SIZE, 0), (CELL_SIZE, HEIGHT), 2)
    pygame.draw.line(screen, BLACK, (2 * CELL_SIZE, 0), (2 * CELL_SIZE, HEIGHT), 2)
    pygame.draw.line(screen, BLACK, (0, CELL_SIZE), (WIDTH, CELL_SIZE), 2)
    pygame.draw.line(screen, BLACK, (0, 2 * CELL_SIZE), (WIDTH, 2 * CELL_SIZE), 2)

    # Малюємо хрестики та нулики
    for row in range(3):
        for col in range(3):
            if game_board[row][col] == "X":
                pygame.draw.line(screen, BLACK, (col * CELL_SIZE, row * CELL_SIZE),
                                 ((col + 1) * CELL_SIZE, (row + 1) * CELL_SIZE), 2)
                pygame.draw.line(screen, BLACK, (col * CELL_SIZE, (row + 1) * CELL_SIZE),
                                 ((col + 1) * CELL_SIZE, row * CELL_SIZE), 2)
            elif game_board[row][col] == "O":
                pygame.draw.circle(screen, BLACK, ((col + 0.5) * CELL_SIZE, (row + 0.5) * CELL_SIZE),
                                   CELL_SIZE // 2, 2)

    pygame.display.flip()

# Перевірка переможця
def check_winner(board):
    # Перевірка по горизонталі
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] is not None:
            return board[row][0]

    # Перевірка по вертикалі
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] is not None:
            return board[0][col]

    # Перевірка по діагоналі
    if board[0][0] == board[1][1] == board[2][2] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] is not None:
        return board[0][2]

    # Перевірка нічиєї
    if all(board[row][col] is not None for row in range(3) for col in range(3)):
        return "DRAW"

    # Гра продовжується
    return None

# Оновлення гри після ходу гравця
def update_game(row, col):
    if game_board[row][col] is None:
        game_board[row][col] = current_player

        winner = check_winner(game_board)
        if winner is not None:
            end_game(winner)
        else:
            change_turn()

# Зміна ходу
def change_turn():
    global current_player
    current_player = "O" if current_player == "X" else "X"

# Закінчення гри
def end_game(winner):
    global game_over
    game_over = True

    if winner == "DRAW":
        message = "It's a draw!"
    else:
        message = f"{winner} wins!"

    pygame.display.set_caption(message)

# Функція для вибору комп'ютером рішення з дерева рішень
def choose_computer_move():
    best_score = -float('inf')
    best_move = None

    for row in range(3):
        for col in range(3):
            if game_board[row][col] is None:
                game_board[row][col] = "O"
                score = minimax(game_board, 0, False)
                game_board[row][col] = None

                if score > best_score:
                    best_score = score
                    best_move = (row, col)

    return best_move

# Рекурсивний алгоритм Мінімакс
def minimax(board, depth, is_maximizing):
    result = check_winner(board)
    if result is not None:
        if result == "X":
            return -1
        elif result == "O":
            return 1
        else:
            return 0

    if is_maximizing:
        best_score = -float('inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] is None:
                    board[row][col] = "O"
                    score = minimax(board, depth + 1, False)
                    board[row][col] = None
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] is None:
                    board[row][col] = "X"
                    score = minimax(board, depth + 1, True)
                    board[row][col] = None
                    best_score = min(score, best_score)
        return best_score

# Головний цикл гри
def run_game():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouse_pos = pygame.mouse.get_pos()
                col = mouse_pos[0] // CELL_SIZE
                row = mouse_pos[1] // CELL_SIZE
                update_game(row, col)
                if not game_over:
                    computer_move = choose_computer_move()
                    if computer_move:
                        update_game(computer_move[0], computer_move[1])

        update_screen()

run_game()
