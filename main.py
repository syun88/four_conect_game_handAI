# Four Python Game
import pygame
import numpy as np
import sys
import os
import time
from gtts import gTTS
from pygame import mixer

# import random
import math

# Welcome to Connect Four Python Game
welcome = "Welcome to Connect Four Python Game"
print(welcome)


def speach(txt):
    tts1 = gTTS(text=txt, lang="ja")
    if not os.path.exists(f"./fou_coin/mp3_file/{txt}.mp3"):
        print("音声データ作成しました")
        tts1.save(f"./fou_coin/mp3_file/{txt}.mp3")
    print("use mp3 file")
    mixer.init()
    mixer.music.load(f"./fou_coin/mp3_file/{txt}.mp3")
    mixer.music.play()
    time.sleep(3)


speach(welcome)

time_text = "please input restart time must over zero:"
speach(time_text)
t = input(time_text)
if t == "":
    print("defult restart time is 5 sec")
    t = 5
else:
    t = int(t)
# ボードの大きさ
row_count = 6
column_count = 7
BLUE = (0, 0, 255)  # color setting
BLACK = (0, 0, 0)  # color setting
RED = (255, 0, 0)  # color setting
YELLOW = (255, 255, 0)  # color setting


##################################
def creat_board():
    board = np.zeros((row_count, column_count))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece



def is_volid_loction(board, col):
    return board[row_count - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(row_count):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))


def winning_move(bord, piece):
    # 横連続 WIN判断
    for c in range(column_count - 3):
        for r in range(row_count):
            if (
                board[r][c] == piece
                and board[r][c + 1] == piece
                and board[r][c + 2] == piece
                and board[r][c + 3] == piece
            ):
                return True
    # 縦連続 WIN判断
    for c in range(column_count):
        for r in range(row_count - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c] == piece
                and board[r + 2][c] == piece
                and board[r + 3][c] == piece
            ):
                return True
    # 正の傾きの対角線の判断
    for c in range(column_count - 3):
        for r in range(row_count - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c + 1] == piece
                and board[r + 2][c + 2] == piece
                and board[r + 3][c + 3] == piece
            ):
                return True
    # 負の傾きの対角線の判断

    for c in range(column_count - 3):
        for r in range(3, row_count):
            if (
                board[r][c] == piece
                and board[r - 1][c + 1] == piece
                and board[r - 2][c + 2] == piece
                and board[r - 3][c + 3] == piece
            ):
                return True


def draw_board(board):
    for c in range(column_count):
        for r in range(row_count):
            pygame.draw.rect(
                screen,
                BLUE,
                (c * squaresize, r * squaresize + squaresize, squaresize, squaresize),
            )
            pygame.draw.circle(
                screen,
                BLACK,
                (
                    (
                        int(c * squaresize + squaresize / 2),
                        int(r * squaresize + squaresize + squaresize / 2),
                    )
                ),
                radius,
            )
    for c in range(column_count):
        for r in range(row_count):
            if board[r][c] == 1:
                pygame.draw.circle(
                    screen,
                    RED,
                    (
                        (
                            int(c * squaresize + squaresize / 2),
                            height - int(r * squaresize + squaresize / 2),
                        )
                    ),
                    radius,
                )
            elif board[r][c] == 2:
                pygame.draw.circle(
                    screen,
                    YELLOW,
                    (
                        (
                            int(c * squaresize + squaresize / 2),
                            height - int(r * squaresize + squaresize / 2),
                        )
                    ),
                    radius,
                )
    pygame.display.update()


board = creat_board()
print(board)
game_over = False
turn = 0

pygame.init()

squaresize = 100
width = column_count * squaresize
height = (row_count + 1) * squaresize
size = (width, height)
radius = int(squaresize / 2 - 5)

chek_board=[]
chek_board.append([0])
chek_board.append([1])
screen = pygame.display.set_mode(size)
draw_board(board)
# sysfont = pygame.font.SysFont(None, 75) #defults フォント設定 英語のみ
sysfont = pygame.font.Font("C:/Windows/Fonts/HGRPP1.TTC", 75)
pygame.display.update()
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, squaresize))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(squaresize / 2)), radius)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(squaresize / 2)), radius)

        pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, squaresize))
            # print("左クリックした座標:"+str(event.pos))
            # player 1 input
            if turn == 0:
                chek_board[0]=board.tolist()
                posx = event.pos[0]
                col = int(math.floor(posx / squaresize))

                # col = int(input("Player 1 Make your selection (0-6):") )
                if is_volid_loction(board, col):
                    
                    row = get_next_open_row(board, col)
                    print(row)
                    drop_piece(board, row, col, 1)
                    draw_board(board)
                    if winning_move(board, 1):
                        player_1_win = "Player1 WIN"
                        print(player_1_win + "!!!")
                        label = sysfont.render(player_1_win, 1, RED)
                        screen.blit(label, (40, 10))
                        pygame.display.update()

                        speach(player_1_win)
                        game_over = True
            # player 2 input
            else:
                chek_board[0]=board.tolist()
                posx = event.pos[0]
                col = int(math.floor(posx / squaresize))
                # col = int(input("Player 2 Make your selection (0-6):") )
                if is_volid_loction(board, col):
                    
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)
                    draw_board(board)
                    if winning_move(board, 2):
                        player_2_win = "Player2 WIN"
                        print(player_2_win + "!!!")
                        label = sysfont.render(player_2_win, 1, YELLOW)
                        screen.blit(label, (40, 10))
                        pygame.display.update()
                        speach(player_2_win)
                        game_over = True
            print_board(board)
            #print_board(board_copy1)
            
            
            chek_board[1]=board.tolist()
            #print(chek_board[0])
            #print(chek_board[1])
            """if board_copy is board_copy1:
                continue
            else:
                """
            if chek_board[0] == chek_board[-1]:
                continue
            else:
                turn += 1
                turn = turn % 2
                
            
        if game_over:
            # t = 10
            save_time=t
            while t > 0:
                pygame.draw.rect(screen, BLACK, (0, 0, width, squaresize))
                # print(t)

                label = sysfont.render(f"{t}sec RESET", 1, BLUE)
                screen.blit(label, (40, 10))
                pygame.display.update()
                time.sleep(1)
                t -= 1
            time.sleep(1)
            t=save_time
            # pygame.time.wait(5000)
            game_over = False
            turn = 0
            board = creat_board()
            print(board)
            draw_board(board)
            pygame.display.update()
