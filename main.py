import pygame
import numpy as np

pygame.init()

# Constants

# Colors 
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)


# Screen
WIDTH, HEIGHT = 300, 300
LIINE_WIDTH = 5
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRICLE_WIDTH = 15
CROSS_WIDTH = 25



# Variables

# Pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe With MiniMax")
screen.fill(BLACK)

board: np.ndarray = np.zeros((BOARD_ROWS, BOARD_COLS))


# Functions
def drawLines(color: tuple[int] = WHITE):
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, color, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LIINE_WIDTH)
        pygame.draw.line(screen, color, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), LIINE_WIDTH)


def drawFigures(color: tuple[int] = WHITE):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, color, 
                    (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), 
                     int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), 
                    CIRCLE_RADIUS, CIRICLE_WIDTH)
            
            elif board[row][col] == 2:
                # Calculate center point
                center_x = col * SQUARE_SIZE + SQUARE_SIZE // 2
                center_y = row * SQUARE_SIZE + SQUARE_SIZE // 2
                # Calculate offset for X size
                offset = SQUARE_SIZE // 3
                
                pygame.draw.line(screen, color, 
                    (center_x - offset, center_y - offset),
                    (center_x + offset, center_y + offset), 
                    CROSS_WIDTH)
                
                pygame.draw.line(screen, color,
                    (center_x - offset, center_y + offset),
                    (center_x + offset, center_y - offset),
                    CROSS_WIDTH)
def markSquare(row: int, col: int, player: int):
    board[row][col] = player


def isSquareEmpty(row: int, col: int, checkBoard: np.ndarray = board) -> bool:
    return checkBoard[row][col] == 0

def isBoardFull(checkBoard: np.ndarray = board) -> bool:
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if checkBoard[row][col] == 0:
                return False

    return True

def checkWin(player: int, checkBoard: np.ndarray = board) -> bool:
    for col in range(BOARD_COLS):
        if checkBoard[0][col] == player and checkBoard[1][col] == player and checkBoard[2][col] == player:
            return True
    
    for row in range(BOARD_ROWS):
        if checkBoard[row][0] == player and checkBoard[row][1] == player and checkBoard[row][2] == player:
            return True
    
    if checkBoard[0][0] == player and checkBoard[1][1] == player and checkBoard[2][2] == player:
        return True

    if checkBoard[0][2] == player and checkBoard[1][1] == player and checkBoard[2][0] == player:
        return True

    return False

def minimax(minimaxBoard, depth, isMaximizing) -> int | float:
    if checkWin(2, minimaxBoard):
        return float('inf')

    if checkWin(1, minimaxBoard):
        return float('-inf')

    if isBoardFull(minimaxBoard):  # Fixed condition
        return 0

    if isMaximizing:
        bestScore = -np.inf

        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if isSquareEmpty(row, col, minimaxBoard):
                    minimaxBoard[row][col] = 2
                    score = minimax(minimaxBoard, depth + 1, False)
                    minimaxBoard[row][col] = 0
                    bestScore = max(score, bestScore)  # Fixed max operation
        
        return bestScore

    else:
        bestScore = np.inf

        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if isSquareEmpty(row, col, minimaxBoard):
                    minimaxBoard[row][col] = 1
                    score = minimax(minimaxBoard, depth + 1, True)
                    minimaxBoard[row][col] = 0
                    bestScore = min(score, bestScore)
        
        return bestScore

def bestMove() -> bool:
    bestScore = -np.inf
    bestMove: tuple[int] = (-1, -1)
    
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if isSquareEmpty(row, col):
                board[row][col] = 2
                score: int | float = minimax(board, 0, False)
                board[row][col] = 0
                if score > bestScore:
                    bestScore = score
                    bestMove = (row, col)
    
    # I don't agree with these design choices, but this is what the tutorial does
    if bestMove != (-1, -1):
        markSquare(bestMove[0], bestMove[1], 2)
        return True

    return False

def restartGame():
    screen.fill(BLACK)
    drawLines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0

def main():
    drawLines()

    player = 1
    gameOver = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN and not gameOver:
                mouseX: int = event.pos[0]
                mouseY: int = event.pos[1]

                clickedRow: int = mouseY // SQUARE_SIZE
                clickedCol: int = mouseX // SQUARE_SIZE

                if isSquareEmpty(clickedRow, clickedCol):
                    markSquare(clickedRow, clickedCol, player)
                    
                    if checkWin(player):
                        gameOver = True
                    player = 2 if player == 1 else 1

                    if not gameOver:
                        if bestMove():
                            if checkWin(2):
                                gameOver = True

                            player = 2 if player == 1 else 1

                    if not gameOver and isBoardFull():
                        gameOver = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restartGame()
                    gameOver = False
                    player = 1

        if not gameOver:
            drawFigures()
        else:
            if checkWin(1):
                drawFigures(GREEN)
                drawLines(GREEN)
            elif checkWin(2):
                drawFigures(RED)
                drawLines(RED)
            else:
                drawFigures(GRAY)
                drawLines(GRAY)

        pygame.display.update()

if __name__ == "__main__":
    main()