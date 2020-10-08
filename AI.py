import numpy as np
import pygame
import math
from pygame import mixer
import random

ROW_COUNT = 8
COLUMN_COUNT = 8
SQUARESIZE = 80
DARK_GREEN = (123, 164, 40)
LIGHT_GREEN = (139, 185, 45)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

white_disc = pygame.image.load("white.png")
black_disc = pygame.image.load("black.png")
icon = pygame.image.load("icon.png")

pygame.init()
screen = pygame.display.set_mode((658, 806))
pygame.display.set_caption("othello")
pygame.display.set_icon(icon)


def indexToPosition(i, j):
    pos = [0, 0]
    pos[0] = SQUARESIZE * j + (2 * (j + 1))
    pos[1] = 150 + (SQUARESIZE * i) + (2 * i)
    return pos


def positionToIndex(x, y):
    index = [0, 0]
    index[0] = int(math.floor((x - 2) / (SQUARESIZE + 2)))
    index[1] = math.floor((y - 150) / (SQUARESIZE + 2))
    return index


def create_board():
    # 1 stands for black
    # 2 stands for white
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    board[3][3] = 1
    board[3][4] = 2
    board[4][3] = 2
    board[4][4] = 1
    return board


def create_hints(board, turn):
    hints = np.zeros((ROW_COUNT, COLUMN_COUNT))
    possibleMoves = []
    for i in range(8):
        for j in range(8):
            if validMove(board, i, j, turn):
                hints[i][j] = 1
                possibleMoves.append([i, j])
    return hints, possibleMoves


def draw_board():
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, LIGHT_GREEN,
                             (c * SQUARESIZE + 2 * (c + 1), (r * SQUARESIZE) + (2 * r) + 150, SQUARESIZE, SQUARESIZE))

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pos = indexToPosition(r, c)
                screen.blit(black_disc, (pos[0], pos[1]))
            elif board[r][c] == 2:
                pos = indexToPosition(r, c)
                screen.blit(white_disc, (pos[0], pos[1]))
            if hints[r][c] == 1:
                pygame.draw.rect(screen, (255, 255, 153),
                                 (c * SQUARESIZE + 2 * (c + 1), (r * SQUARESIZE) + (2 * r) + 150, SQUARESIZE,
                                  SQUARESIZE))
                #  pos = indexToPosition(r, c)
                # screen.blit(dot, (pos[0], pos[1]))
                pass


def draw_score(turn):
    if turn == 1:
        t = "black"
    else:
        t = "white"
    scores = getScore()
    font = pygame.font.SysFont(None, 30)
    black_score = font.render("black score : " + str(scores[0]), True, (255, 255, 255))
    white_score = font.render("white score : " + str(scores[1]), True, (255, 255, 255))
    current_turn = font.render("turn : " + t, True, (255, 255, 255))
    screen.blit(black_score, (10, 10))
    screen.blit(white_score, (10, 40))
    screen.blit(current_turn, (10, 70))

    pass


def validMove(board, x, y, turn):
    # Returns False if the player's move on space xstart, ystart is invalid.
    # If it is a valid move, returns a list of spaces that would become the player's if they made a move here.
    if board[x][y] != 0:
        return False
    # board[x][y] = turn  # temporarly

    flip_E = []
    flip_W = []
    flip_N = []
    flip_S = []
    flip_SE = []
    flip_SW = []
    flip_NE = []
    flip_NW = []

    if turn == 1:
        other = 2
    else:
        other = 1

    for i in range(x + 1, 8):  # south

        if board[i][y] == other:
            if i == 7:
                flip_S.clear()
                break
            flip_S.append([i, y])
            continue
        if board[i][y] == 0:
            flip_S.clear()
            break
        if board[i][y] == turn:
            break

    for i in range(x - 1, -1, -1):  # north
        if board[i][y] == other:
            if i == 0:
                flip_N.clear()
                break
            flip_N.append([i, y])
            continue
        if board[i][y] == 0:
            flip_N.clear()
            break
        if board[i][y] == turn:
            break
    for i in range(y + 1, 8):  # east
        if board[x][i] == other:
            if i == 7:
                flip_E.clear()
                break
            flip_E.append([x, i])
            continue
        if board[x][i] == 0:
            flip_E.clear()
            break
        if board[x][i] == turn:
            break
    for i in range(y - 1, -1, -1):  # west
        if board[x][i] == other:
            if i == 0:
                flip_W.clear()
                break
            flip_W.append([x, i])
            continue
        if board[x][i] == 0:
            flip_W.clear()
            break
        if board[x][i] == turn:
            break

    i = x
    j = y
    while i != 7 and j != 7:  # south east
        i += 1
        j += 1
        if board[i][j] == other:
            if i == 7 or j == 7:
                flip_SE.clear()
                break
            flip_SE.append([i, j])
            continue
        if board[i][j] == 0:
            flip_SE.clear()
            break
        if board[i][j] == turn:
            break

    i = x
    j = y
    while i != 7 and j != 0:  # south west
        i += 1
        j -= 1
        if board[i][j] == other:
            if i == 7 or j == 0:
                flip_SW.clear()
                break
            flip_SW.append([i, j])
            continue
        if board[i][j] == 0:
            flip_SW.clear()
            break
        if board[i][j] == turn:
            break

    i = x
    j = y
    while i != 0 and j != 0:  # north west
        i -= 1
        j -= 1
        if board[i][j] == other:
            if i == 0 or j == 0:
                flip_NW.clear()
                break
            flip_NW.append([i, j])
            continue
        if board[i][j] == 0:
            flip_NW.clear()
            break
        if board[i][j] == turn:
            break

    i = x
    j = y
    while i != 0 and j != 7:  # north east
        i -= 1
        j += 1
        if board[i][j] == other:
            if i == 0 or j == 7:
                flip_NE.clear()
                break
            flip_NE.append([i, j])
            continue
        if board[i][j] == 0:
            flip_NE.clear()
            break
        if board[i][j] == turn:
            break

    tilesToFlip = []
    tilesToFlip.extend(flip_S)
    tilesToFlip.extend(flip_N)
    tilesToFlip.extend(flip_E)
    tilesToFlip.extend(flip_W)
    tilesToFlip.extend(flip_SE)
    tilesToFlip.extend(flip_SW)
    tilesToFlip.extend(flip_NE)
    tilesToFlip.extend(flip_NW)

    if len(tilesToFlip) == 0:
        return False
    else:
        return tilesToFlip


def getScore():
    scores = [0, 0]
    for i in range(8):
        for j in range(8):
            if board[i][j] == 1:
                scores[0] += 1
            elif board[i][j] == 2:
                scores[1] += 1
    return scores


def game_over():
    font = pygame.font.SysFont(None, 30)
    for i in range(8):
        for j in range(8):
            if validMove(board, i, j, 1) != False or validMove(board, i, j, 2) != False:
                return False
    scores = getScore()
    if scores[0] > scores[1]:
        gameOver = font.render("BLACK WON!!", True, (255, 0, 0))
        print("player white won!")
        screen.blit(gameOver, (10, 100))
    else:
        gameOver = font.render("WHITE WON!!", True, (255, 0, 0))
        print("player white won!")
        screen.blit(gameOver, (10, 100))

    return True


def evaluator(board):
    heuristic = np.array([[1000, -10, 10, 10, 10, 10, -10, 1000],
                          [-10, -10, 1, 1, 1, 1, -10, -10],
                          [10, 1, 1, 1, 1, 1, 1, 10],
                          [10, 1, 1, 1, 1, 1, 1, 10],
                          [10, 1, 1, 1, 1, 1, 1, 10],
                          [10, 1, 1, 1, 1, 1, 1, 10],
                          [-10, -10, 1, 1, 1, 1, -10, -10],
                          [1000, -10, 10, 10, 10, 10, -10, 1000]])
    human_score = 0
    AI_score = 0
    human_weighted = 0
    AI_weighted = 0
    empty = 0
    for i in range(8):
        for j in range(8):
            if board[i][j] == 0:
                empty += 1
            if board[i][j] == 1:
                human_score += 1
                human_weighted += heuristic[i][j]
            if board[i][j] == 2:
                AI_score += 1
                AI_weighted += heuristic[i][j]
    if empty > 0:
        return AI_weighted, human_weighted  # mikhahad tafavote score beine human va robo ta jai ke mishe bishtar beshe
    else:
        return AI_score, human_score


def minimax_minimizer(board, turn, depth, alpha, beta):
    possible_moves = create_hints(board, turn)[1]
    if len(possible_moves) == 0 or running == False or depth == 0:
        score = evaluator(board)
        if turn == 2:
            score = score[0] - score[1]
            return score
        else:
            score = score[1] - score[0]
            return score
    else:
        if turn == 1:
            next_turn = 2
        else:
            next_turn = 1

    min_score = math.inf
    for move in possible_moves:
        new_board = np.copy(board)
        tilesToFlip = validMove(board, move[0], move[1], turn)
        new_board[move[0]][move[1]] = turn
        flip(new_board, tilesToFlip, turn)
        score = minimax_maximizer(new_board, next_turn, depth - 1, alpha, beta)
        if score < min_score:
            min_score = score
        beta = min(beta, score)
        if beta <= alpha:
            break
    return min_score


def minimax_maximizer(board, turn, depth, alpha, beta):
    possible_moves = create_hints(board, turn)[1]
    if len(possible_moves) == 0 or running == False or depth == 0:
        score = evaluator(board)
        if turn == 2:
            score = score[0] - score[1]
            return score
        else:
            score = score[1] - score[0]
            return score
    else:
        if turn == 1:
            next_turn = 2
        else:
            next_turn = 1

    max_score = -math.inf
    for move in possible_moves:
        new_board = np.copy(board)
        tilesToFlip = validMove(board, move[0], move[1], turn)
        new_board[move[0]][move[1]] = turn
        flip(new_board, tilesToFlip, turn)
        score = minimax_minimizer(new_board, next_turn, depth - 1, alpha, beta)
        if score > max_score:
            max_score = score
            if depth == AI_DEPTH:
                print("best move: " + str(move))
                setBestMove(move)  # fagaht bayad az beine omghe avali ha peida kone!!!
        alpha = max(alpha, score)
        if beta <= alpha:
            break
    return max_score


def setBestMove(move):
    best_move[0] = move[0]
    best_move[1] = move[1]


def flip(board, tiles, turn):
    for i in range(len(tiles)):
        board[tiles[i][0]][tiles[i][1]] = turn
    pass


best_move = [0, 0]
# turn = random.randint(1, 2)
turn = 1
board = create_board()
running = True
AI_DEPTH = 2

while running:
    screen.fill((25, 0, 51))
    hints = create_hints(board, turn)[0]
    possible_moves = create_hints(board, turn)[1]

    draw_board()
    draw_score(turn)

    if game_over():
        running = False
        draw_board()
        pygame.display.update()
        pygame.time.wait(5000)

    # change the turn if there is not any possible moves
    if len(possible_moves) == 0:
        if turn == 1:
            print("player black can't make any moves! turn changed!")
            turn = 2
        else:
            print("player white can't make any moves! turn changed!")
            turn = 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x = event.pos[0]
            y = event.pos[1]
            j, i = positionToIndex(x, y)

            if turn == 1:
                tilesToFlip = validMove(board, i, j, 1)
                if tilesToFlip:
                    board[i][j] = 1
                    flip(board, tilesToFlip, turn)
                    flip_sound = mixer.Sound('flip.wav')
                    flip_sound.play()

                    hints = np.zeros((ROW_COUNT, COLUMN_COUNT))
                    draw_board()
                    # draw_score(turn)
                    pygame.display.update()
                    turn = 2

    if turn == 2:
        pygame.time.wait(1000)
        alpha = -math.inf
        beta = math.inf
        minimax_maximizer(board, turn, AI_DEPTH, alpha, beta)  # finds the best move
        tilesToFlip = validMove(board, best_move[0], best_move[1], 2)
        if tilesToFlip:
            board[best_move[0]][best_move[1]] = 2
            flip(board, tilesToFlip, turn)
            flip_sound = mixer.Sound('flip.wav')
            flip_sound.play()
        turn = 1

    pygame.display.update()
