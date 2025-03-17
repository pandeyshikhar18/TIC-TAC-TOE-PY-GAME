import pygame
import sys
import random

pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
CELL_SIZE = WIDTH // BOARD_COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)

# Initialize display and font
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")
font = pygame.font.SysFont(None, 50)

# Game board (2D list)
board = [[None] * BOARD_COLS for _ in range(BOARD_ROWS)]

# Global variables for settings
player = None      # human player's symbol
ai_player = None   # AI's symbol
difficulty = None  # 'easy', 'medium', 'hard'
game_over = False

# ------------------ Drawing Functions ------------------
def draw_lines():
    """Fill the background and draw the grid."""
    screen.fill(WHITE)
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures():
    """Draw X's and O's based on board state."""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'X':
                pygame.draw.line(screen, RED, 
                                 (col * CELL_SIZE + 50, row * CELL_SIZE + 50),
                                 ((col + 1) * CELL_SIZE - 50, (row + 1) * CELL_SIZE - 50), 
                                 LINE_WIDTH)
                pygame.draw.line(screen, RED, 
                                 ((col + 1) * CELL_SIZE - 50, row * CELL_SIZE + 50),
                                 (col * CELL_SIZE + 50, (row + 1) * CELL_SIZE - 50), 
                                 LINE_WIDTH)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, BLACK, 
                                   (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
                                   CELL_SIZE // 3, LINE_WIDTH)

def draw_winning_line(winner_combo):
    (start_row, start_col), (end_row, end_col) = winner_combo
    start_pos = (start_col * CELL_SIZE + CELL_SIZE // 2, start_row * CELL_SIZE + CELL_SIZE // 2)
    end_pos = (end_col * CELL_SIZE + CELL_SIZE // 2, end_row * CELL_SIZE + CELL_SIZE // 2)
    pygame.draw.line(screen, GREEN, start_pos, end_pos, LINE_WIDTH + 5)

# ------------------ Game Logic ------------------
def check_winner():
    # Check rows
    for row in range(BOARD_ROWS):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] is not None:
            return board[row][0], [(row, 0), (row, 2)]
    # Check columns
    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            return board[0][col], [(0, col), (2, col)]
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0], [(0, 0), (2, 2)]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2], [(0, 2), (2, 0)]
    return None, []

def display_message(message):
    """Show a message (win/draw) on screen for 2 seconds."""
    text = font.render(message, True, RED)
    screen.fill(WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(2000)

def reset_game():
    """Reset board and game state, and redraw grid."""
    global board, game_over
    board = [[None] * BOARD_COLS for _ in range(BOARD_ROWS)]
    game_over = False
    draw_lines()

# ------------------ AI Functions ------------------
def ai_move():
    """AI move based on selected difficulty."""
    empty_cells = [(r, c) for r in range(BOARD_ROWS) for c in range(BOARD_COLS) if board[r][c] is None]
    if not empty_cells:
        return
    if difficulty == 'easy':
        row, col = random.choice(empty_cells)
        board[row][col] = ai_player
    elif difficulty == 'medium':
        # Try to win
        for r, c in empty_cells:
            board[r][c] = ai_player
            if check_winner()[0] == ai_player:
                return
            board[r][c] = None
        # Try to block opponent win
        for r, c in empty_cells:
            board[r][c] = player
            if check_winner()[0] == player:
                board[r][c] = ai_player
                return
            board[r][c] = None
        # Else, random move
        row, col = random.choice(empty_cells)
        board[row][col] = ai_player
    elif difficulty == 'hard':
        row, col = best_move()
        board[row][col] = ai_player

def best_move():
    best_score = -float('inf')
    move = None
    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            if board[r][c] is None:
                board[r][c] = ai_player
                score = minimax(board, 0, False)
                board[r][c] = None
                if score > best_score:
                    best_score = score
                    move = (r, c)
    return move

def minimax(board_state, depth, is_maximizing):
    winner, _ = check_winner()
    if winner == ai_player:
        return 10 - depth
    elif winner == player:
        return depth - 10
    elif all(cell is not None for row in board_state for cell in row):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS):
                if board_state[r][c] is None:
                    board_state[r][c] = ai_player
                    score = minimax(board_state, depth + 1, False)
                    board_state[r][c] = None
                    best_score = max(best_score, score)
        return best_score
    else:
        best_score = float('inf')
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS):
                if board_state[r][c] is None:
                    board_state[r][c] = player
                    score = minimax(board_state, depth + 1, True)
                    board_state[r][c] = None
                    best_score = min(best_score, score)
        return best_score

# ------------------ Menu Screens ------------------
def level_selection_screen():
    """Display level selection screen with clickable buttons."""
    global difficulty
    selecting = True
    while selecting:
        screen.fill(WHITE)
        title = font.render("Select Difficulty", True, BLACK)
        # Define button rectangles
        easy_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 100, 200, 50)
        medium_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2, 200, 50)
        hard_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 100, 200, 50)
        # Draw buttons
        pygame.draw.rect(screen, GREEN, easy_rect)
        pygame.draw.rect(screen, RED, medium_rect)
        pygame.draw.rect(screen, BLACK, hard_rect)
        # Render text
        easy_text = font.render("Easy", True, WHITE)
        medium_text = font.render("Medium", True, WHITE)
        hard_text = font.render("Hard", True, WHITE)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//4))
        screen.blit(easy_text, (easy_rect.centerx - easy_text.get_width()//2, easy_rect.centery - easy_text.get_height()//2))
        screen.blit(medium_text, (medium_rect.centerx - medium_text.get_width()//2, medium_rect.centery - medium_text.get_height()//2))
        screen.blit(hard_text, (hard_rect.centerx - hard_text.get_width()//2, hard_rect.centery - hard_text.get_height()//2))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if easy_rect.collidepoint(pos):
                    difficulty = 'easy'
                    selecting = False
                elif medium_rect.collidepoint(pos):
                    difficulty = 'medium'
                    selecting = False
                elif hard_rect.collidepoint(pos):
                    difficulty = 'hard'
                    selecting = False

def symbol_selection_screen():
    """Display symbol selection screen with clickable buttons."""
    global player, ai_player
    selecting = True
    while selecting:
        screen.fill(WHITE)
        title = font.render("Choose Your Symbol", True, BLACK)
        # Define button rectangles for X and O
        x_rect = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 - 25, 130, 50)
        o_rect = pygame.Rect(WIDTH//2 + 20, HEIGHT//2 - 25, 130, 50)
        pygame.draw.rect(screen, RED, x_rect)
        pygame.draw.rect(screen, GREEN, o_rect)
        x_text = font.render("Play as X", True, WHITE)
        o_text = font.render("Play as O", True, WHITE)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//4))
        screen.blit(x_text, (x_rect.centerx - x_text.get_width()//2, x_rect.centery - x_text.get_height()//2))
        screen.blit(o_text, (o_rect.centerx - o_text.get_width()//2, o_rect.centery - o_text.get_height()//2))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if x_rect.collidepoint(pos):
                    player, ai_player = 'X', 'O'
                    selecting = False
                elif o_rect.collidepoint(pos):
                    player, ai_player = 'O', 'X'
                    selecting = False

def restart_screen(message):
    """Display end-of-game message with a restart button. Clicking restart returns to level selection."""
    waiting = True
    while waiting:
        screen.fill(WHITE)
        msg_text = font.render(message, True, RED)
        restart_text = font.render("Restart", True, WHITE)
        # Define a restart button rectangle
        restart_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2, 200, 50)
        pygame.draw.rect(screen, GREEN, restart_rect)
        screen.blit(msg_text, (WIDTH//2 - msg_text.get_width()//2, HEIGHT//3))
        screen.blit(restart_text, (restart_rect.centerx - restart_text.get_width()//2, restart_rect.centery - restart_text.get_height()//2))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if restart_rect.collidepoint(pos):
                    waiting = False

# ------------------ Main Program ------------------
def main():
    global game_over
    # Show level and symbol selection screens
    level_selection_screen()
    symbol_selection_screen()
    reset_game()
    # If player is O, let the AI start (since X traditionally goes first)
    if player == 'O':
        ai_move()
    
    running = True
    while running:
        draw_lines()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                pos = pygame.mouse.get_pos()
                row = pos[1] // CELL_SIZE
                col = pos[0] // CELL_SIZE
                if board[row][col] is None:
                    board[row][col] = player
                    if not check_winner()[0] and any(None in row for row in board):
                        ai_move()
        # Redraw the figures
        draw_figures()
        pygame.display.update()
        
        # Check for a winner
        winner, combo = check_winner()
        if winner:
            draw_winning_line(combo)
            draw_figures()
            pygame.display.update()
            restart_screen(f"{winner} wins!")
            level_selection_screen()
            symbol_selection_screen()
            reset_game()
            if player == 'O':
                ai_move()
        elif all(cell is not None for row in board for cell in row):
            pygame.display.update()
            restart_screen("It's a draw!")
            level_selection_screen()
            symbol_selection_screen()
            reset_game()
            if player == 'O':
                ai_move()

if __name__ == '__main__':
    main()
