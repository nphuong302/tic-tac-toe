import pygame
import sys
from pygame.locals import *
import time

pygame.init()
WIDTH = 600
win = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Tic Tac Toe")
fps = 30
frame = pygame.time.Clock()

# Colors

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Window
# initiating_window = pygame.transform.scale(pygame.image.load("background.png"), (WIDTH, WIDTH))
x_img = pygame.transform.scale(pygame.image.load("x.png"), (100, 100))
o_img = pygame.transform.scale(pygame.image.load("o.png"), (100, 100))


# Font 

END_FONT = pygame.font.SysFont("Helvetica", 40)

# Functions

def draw_board():
    win.fill(WHITE)
    # win.blit(initiating_window, (0,0))
    pygame.display.update()
    time.sleep(1)
    # win.fill(WHITE)

    # Draw vertical, horizontal lines
    for i in range (1, 3):
        pygame.draw.line(win, BLACK, (i * WIDTH / 3, 0), (i * WIDTH / 3, WIDTH), 5)
        pygame.draw.line(win, BLACK, (0, i * WIDTH / 3), (WIDTH, i * WIDTH / 3), 5)

    pygame.display.flip()

def initialize_grid():
    global dis_to_cen
    dis_to_cen = WIDTH // 3 // 2
    grid = [[None for _ in range(3)] for _ in range(3)]
    
    for i in range(3):
        for j in range(3):
            x = (2 * i + 1) * dis_to_cen
            y = (2 * j + 1) * dis_to_cen
            grid[i][j] = (x, y, "", True)
    return grid

def click(grid, x_turn, o_turn):
    r_x, r_y = pygame.mouse.get_pos()
    for i in range(3):
        for j in range(3):
            x, y, char, can_play = grid[i][j]
    
    # calculate distance:
            dis = ((r_x - x)**2 + (r_y - y)**2) ** 0.5
    
            if dis <= dis_to_cen and can_play:
                if x_turn:
                    char = "X"
                    win.blit(x_img, (x - 50, y - 50))
                    x_turn = False
                    o_turn = True
                else:
                    char = "O"
                    win.blit(o_img, (x - 50, y - 50))
                    x_turn = True
                    o_turn = False
                grid[i][j] = (x, y, char, False)
                pygame.display.update()
                return grid, x_turn, o_turn
    return grid, x_turn, o_turn

def check_win(grid):
    winner = None
    
    # Check row
    for r in range(3):
        if (grid[r][0][2] == grid[r][1][2] == grid[r][2][2]) and (grid[r][0][2] != ""):
            winner = grid[r][0][2]
            return winner
    
    # Check column
    for c in range(3):
        if (grid[0][c][2] == grid[1][c][2] == grid[2][c][2]) and (grid[0][c][2] != ""):
            winner = grid[0][c][2]
            return winner
    
    # Check diagonal
    if (grid[0][0][2] == grid[1][1][2] == grid[2][2][2]) and (grid[0][0][2] != ""):
        winner = grid[0][0][2]
        return winner
    
    if (grid[0][2][2] == grid[1][1][2] == grid[2][0][2]) and (grid[0][2][2] != ""):
        winner = grid[0][2][2]
        return winner    

def check_full(grid):
    # Check if all cells are filled
    for row in grid:
        for cell in row:
            if cell[2] == "":
                return False
    return True    

def display_message(text):
    win.fill(PURPLE)
    text = END_FONT.render(text, True, WHITE)
    win.blit(text, (WIDTH // 2 - text.get_width() // 2, WIDTH // 2 - text.get_height() // 2))
    pygame.display.update()
    time.sleep(3)

def run():
    global x_turn, o_turn 
    x_turn = True
    o_turn = False
    grid = initialize_grid()    
    draw_board()
    
    # Main display loop to allow user to quit the game
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                # pygame.display.quit()
                pygame.quit()
                quit()
            elif event.type == MOUSEBUTTONDOWN:
                grid, x_turn, o_turn = click(grid, x_turn, o_turn)
                
                winner = check_win(grid)
                if winner:
                    display_message(str(winner) + " has won!")
                    running  = False
                elif check_full(grid):
                    display_message("It's a draw!")
                    running  = False

        pygame.display.flip()
        frame.tick(fps)
        