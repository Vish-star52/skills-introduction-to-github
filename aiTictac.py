import pygame
import numpy as np
import sys
import math
import random

# ------------------- CONFIG -------------------
ROWS = 3
COLS = 3
SQUARE_SIZE = 200
WIDTH = COLS * SQUARE_SIZE
HEIGHT = ROWS * SQUARE_SIZE + 100  # extra for UI
LINE_WIDTH = 10
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
OFFSET = 55

# COLORS
BG_COLOR = (255, 255, 0)
LINE_COLOR = (0, 0, 0)
CIRCLE_COLOR = (255, 105, 180)
CROSS_COLOR = (255, 0, 0)
UI_COLOR = (230, 230, 230)
BUTTON_COLOR = (200, 200, 200)
TEXT_COLOR = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe with AI")
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 60)

# Restart Button
BUTTON_W, BUTTON_H = 160, 50
button_rect = pygame.Rect(WIDTH - BUTTON_W - 20, HEIGHT - 80, BUTTON_W, BUTTON_H)

# ------------------- GAME STATE -------------------
board = np.zeros((ROWS, COLS))
game_over = False
player_turn = True  # True = Human, False = AI
winner = None


# ------------------- DRAW FUNCTIONS -------------------
def draw_lines():
    # Horizontal
    for i in range(1, ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)
    # Vertical
    for j in range(1, COLS):
        pygame.draw.line(screen, LINE_COLOR, (j * SQUARE_SIZE, 0), (j * SQUARE_SIZE, ROWS * SQUARE_SIZE), LINE_WIDTH)


def draw_figures():
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, CIRCLE_COLOR,
                                   (int(col * SQUARE_SIZE + SQUARE_SIZE / 2), int(row * SQUARE_SIZE + SQUARE_SIZE / 2)),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 2:
                start1 = (col * SQUARE_SIZE + OFFSET, row * SQUARE_SIZE + OFFSET)
                end1 = (col * SQUARE_SIZE + SQUARE_SIZE - OFFSET, row * SQUARE_SIZE + SQUARE_SIZE - OFFSET)
                start2 = (col * SQUARE_SIZE + OFFSET, row * SQUARE_SIZE + SQUARE_SIZE - OFFSET)
                end2 = (col * SQUARE_SIZE + SQUARE_SIZE - OFFSET, row * SQUARE_SIZE + OFFSET)
                pygame.draw.line(screen, CROSS_COLOR, start1, end1, CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, start2, end2, CROSS_WIDTH)


def draw_ui():
    pygame.draw.rect(screen, UI_COLOR, (0, ROWS * SQUARE_SIZE, WIDTH, 100))
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    pygame.draw.rect(screen, LINE_COLOR, button_rect, 2)
    btn_text = font.render("REFRESH", True, TEXT_COLOR)
    screen.blit(btn_text, (button_rect.x + 30, button_rect.y + 10))

    info_text = "Your Turn" if player_turn and not game_over else "AI Thinking..." if not player_turn and not game_over else ""
    if info_text:
        info_surface = font.render(info_text, True, TEXT_COLOR)
        screen.blit(info_surface, (20, HEIGHT - 70))


def show_result():
    msg = "Draw!" if winner == 0 else ("You Win!" if winner == 1 else "AI Wins!")
    text_surface = big_font.render(msg, True, TEXT_COLOR)
    rect = text_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 50))
    screen.blit(text_surface, rect)


# ------------------- GAME LOGIC -------------------
def available_moves():
    return [(r, c) for r in range(ROWS) for c in range(COLS) if board[r][c] == 0]


def mark_square(row, col, player):
    board[row][col] = player


def check_win(player):
    # Rows and Cols
    for i in range(ROWS):
        if all(board[i, :] == player) or all(board[:, i] == player):
            return True
    # Diagonals
    if all(board[i, i] == player for i in range(ROWS)) or all(board[i, ROWS - 1 - i] == player for i in range(ROWS)):
        return True
    return False


def is_full():
    return not (board == 0).any()


def minimax(state, depth, is_maximizing):
    # Base conditions
    if check_win(2):  # AI
        return 1
    if check_win(1):  # Player
        return -1
    if is_full():
        return 0

    if is_maximizing:
        best_score = -math.inf
        for (r, c) in available_moves():
            state[r][c] = 2
            score = minimax(state, depth + 1, False)
            state[r][c] = 0
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for (r, c) in available_moves():
            state[r][c] = 1
            score = minimax(state, depth + 1, True)
            state[r][c] = 0
            best_score = min(score, best_score)
        return best_score


def ai_move():
    best_score = -math.inf
    move = None
    for (r, c) in available_moves():
        board[r][c] = 2
        score = minimax(board, 0, False)
        board[r][c] = 0
        if score > best_score:
            best_score = score
            move = (r, c)
    if move:
        mark_square(move[0], move[1], 2)


def reset_game():
    global board, player_turn, game_over, winner
    board = np.zeros((ROWS, COLS))
    player_turn = True
    game_over = False
    winner = None


# ------------------- MAIN LOOP -------------------
screen.fill(BG_COLOR)
draw_lines()
draw_ui()
pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            # Restart button
            if button_rect.collidepoint(mx, my):
                reset_game()
                screen.fill(BG_COLOR)
                draw_lines()

            if not game_over and player_turn and my < ROWS * SQUARE_SIZE:
                row = my // SQUARE_SIZE
                col = mx // SQUARE_SIZE
                if board[row][col] == 0:
                    mark_square(row, col, 1)
                    if check_win(1):
                        winner = 1
                        game_over = True
                    elif is_full():
                        winner = 0
                        game_over = True
                    else:
                        player_turn = False

    # AI Move
    if not player_turn and not game_over:
        pygame.time.wait(500)  # small delay to look natural
        ai_move()
        if check_win(2):
            winner = 2
            game_over = True
        elif is_full():
            winner = 0
            game_over = True
        else:
            player_turn = True

    # Redraw
    screen.fill(BG_COLOR)
    draw_lines()
    draw_figures()
    draw_ui()
    if game_over:
        show_result()
    pygame.display.update()
