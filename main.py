import pygame

WIDTH = 540
HEIGHT = 540
CELL_SIZE = WIDTH // 9

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (134, 174, 240)
DARK_BLUE = (79, 92, 110)
RED = (255,0,0)

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Solver")

font_path = "font.ttf"
font_size = 36
font = pygame.font.Font(font_path, font_size)

board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

selected_cell = (0, 0)
invalid_cell = False

def draw_board():
    window.fill(WHITE)
    
    for i in range(10):
        if i % 3 == 0:
            line_color = BLACK
        else:
            line_color = LIGHT_BLUE
        
        # horizontal lines
        pygame.draw.line(window, line_color, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), 2)
        # vertical lines
        pygame.draw.line(window, line_color, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), 2)
    
    # board numbers
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                number_color = BLACK
                if invalid_cell:
                    number_color = RED
                number = font.render(str(board[i][j]), True, number_color)
                window.blit(number, (j * CELL_SIZE + 20, i * CELL_SIZE + 5))

    # selected cell
    pygame.draw.rect(window, DARK_BLUE, (selected_cell[1] * CELL_SIZE, selected_cell[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)

def solve(board):
    find = find_empty(board)
    if not find:
        return True  # solved
    else:
        row, col = find

    for num in range(1, 10):
        if valid(board, num, (row, col)):
            board[row][col] = num

            if solve(board):
                return True

            board[row][col] = 0
    
    return False  # could not solve

def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)  # row, col

    return None

def valid(board, num, pos):
    # row
    for i in range(len(board[0])):
        if board[pos[0]][i] == num and pos[1] != i:
            return False

    # col
    for i in range(len(board)):
        if board[i][pos[1]] == num and pos[0] != i:
            return False

    # boxes
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False

    return True

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if solve(board):
                    invalid_cell = False
                else:
                    invalid_cell = True
            elif event.key == pygame.K_LEFT:
                selected_cell = (selected_cell[0], (selected_cell[1] - 1) % 9)
            elif event.key == pygame.K_RIGHT:
                selected_cell = (selected_cell[0], (selected_cell[1] + 1) % 9)
            elif event.key == pygame.K_UP:
                selected_cell = ((selected_cell[0] - 1) % 9, selected_cell[1])
            elif event.key == pygame.K_DOWN:
                selected_cell = ((selected_cell[0] + 1) % 9, selected_cell[1])
            elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
                               pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9):
                number = int(event.unicode)
                if valid(board, number, selected_cell):
                    board[selected_cell[0]][selected_cell[1]] = number
                    invalid_cell = False
                else:
                    invalid_cell = True
            elif event.key in (pygame.K_0, pygame.K_BACKSPACE):
                board[selected_cell[0]][selected_cell[1]] = 0
                invalid_cell = False

    
    draw_board()
    pygame.display.update()

pygame.quit()
