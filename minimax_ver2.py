import pygame
import sys
from pygame.locals import *
import math 
import time

# Using depth in score and alpha-beta pruning for this version.

pygame.init()
WIDTH = 600
win = pygame.display.set_mode((WIDTH, WIDTH))
fps = 30
frame = pygame.time.Clock()
pygame.display.set_caption("Tic Tac Toe")

# Colors and font
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.SysFont("Cambria", 40)

# Images
x_img = pygame.transform.scale(pygame.image.load("x.png"), (100, 100))
o_img = pygame.transform.scale(pygame.image.load("o.png"), (100, 100))

player = {"X": -10, "O": 10, "tie": 0}

def draw_board():
    win.fill(WHITE)
    # Draw grid
    for i in range(1, 3):
        pygame.draw.line(win, BLACK, (WIDTH // 3 * i, 0), (WIDTH // 3 * i, WIDTH), 10)
        pygame.draw.line(win, BLACK, (0, WIDTH // 3 * i), (WIDTH, WIDTH // 3 * i), 10)
    pygame.display.update()

def init_grid():
    square = WIDTH // 3
    dis_to_cen = square // 2
    grid = [[(square * i + dis_to_cen, square * j + dis_to_cen, "", True) for j in range(3)] for i in range(3)]
    return grid

def draw_mark(x, y, char):
    if char == "X":
        win.blit(x_img, (x - 50, y - 50))
    elif char == "O":
        win.blit(o_img, (x - 50, y - 50))
    pygame.display.update()

def check_win(grid):
    for r in range(3):
        if grid[r][0][2] == grid[r][1][2] == grid[r][2][2] != "":
            return grid[r][0][2]
    for c in range(3):
        if grid[0][c][2] == grid[1][c][2] == grid[2][c][2] != "":
            return grid[0][c][2]
    if grid[0][0][2] == grid[1][1][2] == grid[2][2][2] != "":
        return grid[0][0][2]
    if grid[0][2][2] == grid[1][1][2] == grid[2][0][2] != "":
        return grid[0][2][2]
    return None

def check_full(grid):
    for row in grid:
        for cell in row:
            if cell[2] == "":
                return False
    return True

# Use depth in score:  
def minimax(grid, depth, is_maximizing, alpha, beta):
    winner = check_win(grid)
    if winner == "O":
        return player[winner] - depth
    elif winner == "X":
        return player[winner] + depth
    if check_full(grid):
        return 0  # Tie score
    
    if is_maximizing:
        best_score = -math.inf
        for i in range(3):
            for j in range(3):
                if grid[i][j][3]:
                    grid[i][j] = (grid[i][j][0], grid[i][j][1], "O", False)
                    score = minimax(grid, depth + 1, False, alpha, beta)
                    grid[i][j] = (grid[i][j][0], grid[i][j][1], "", True)
                    best_score = max(best_score, score)
                    if best_score >= beta: return best_score
                    alpha = max(alpha, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(3):
            for j in range(3):
                if grid[i][j][3]:
                    grid[i][j] = (grid[i][j][0], grid[i][j][1], "X", False)
                    score = minimax(grid, depth + 1, True, alpha, beta)
                    grid[i][j] = (grid[i][j][0], grid[i][j][1], "", True)
                    best_score = min(best_score, score)
                    if best_score <= alpha: return best_score
                    beta = min(beta, best_score)
        return best_score

def ai_move(grid):
    best_score = -math.inf
    best_move = None
    for i in range(3):
        for j in range(3):
            if grid[i][j][2] == "":
                grid[i][j] = (grid[i][j][0], grid[i][j][1], "O", False)
                score = minimax(grid, 0, False, -math.inf, math.inf)
                grid[i][j] = (grid[i][j][0], grid[i][j][1], "", True)
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    if best_move:
        i, j = best_move
        x, y, _, _ = grid[i][j]
        grid[i][j] = (x, y, "O", False)
        draw_mark(x, y, "O")
    return grid

def click(grid, x_turn):
    r_x, r_y = pygame.mouse.get_pos()
    for i in range(3):
        for j in range(3):
            x, y, char, canplay = grid[i][j]
            if canplay and (x - WIDTH // 6 <= r_x <= x + WIDTH // 6) and (y - WIDTH // 6 <= r_y <= y + WIDTH // 6):
                grid[i][j] = (x, y, "X", False)
                draw_mark(x, y, "X")
                return grid, False
    return grid, x_turn

def main():
    x_turn = True
    grid = init_grid()
    draw_board()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if x_turn and event.type == MOUSEBUTTONDOWN:
                grid, x_turn = click(grid, x_turn)

        if not x_turn and running:
            grid = ai_move(grid)
            x_turn = True

        winner = check_win(grid)
        if winner:
            print(f"{winner} wins!")
            time.sleep(1)
            running = False
        elif check_full(grid):
            print("It's a tie!")
            time.sleep(1)
            running = False

        frame.tick(fps)

if __name__ == "__main__":
    while True:
        start_time = time.time()  # Record the start time
        main()
        end_time = time.time()    # Record the end time

        elapsed_time = end_time - start_time
        print(f"Function took {elapsed_time:.6f} seconds")
