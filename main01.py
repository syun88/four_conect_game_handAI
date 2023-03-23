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
import glob
import cv2
import pandas as pd
import mediapipe as mp
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pickle

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
GRAY = (128, 128, 128)  # color setting
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
                GRAY,
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
print(size)
radius = int(squaresize / 2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
# sysfont = pygame.font.SysFont(None, 75)
sysfont = pygame.font.Font("C:/Windows/Fonts/HGRPP1.TTC", 75)
pygame.display.update()

# 後で使う対応表の作成
# label_dict = {0: 'b', 1: 'a', 2: 'c'}
# dic = {"a": "wait_magic", "b": "magic_attack", "c": "magic_defense"}

# 前工程で作ったモデルの取得

with open("./fou_coin/model/logistic.pkl", "rb") as f:
    model = pickle.load(f)

    # 検出器のインスタンス化
    # 検出器のインスタンス化 defult is 0.5 min_detection_confidence=0.5
hands = mp.solutions.hands.Hands(
    static_image_mode=True, max_num_hands=1, min_detection_confidence=0.6
)
cap = cv2.VideoCapture(0)
chek_board = []
chek_board.append([0])
chek_board.append([1])
command_list = []
command_list.append("Start")
command_list.append("Start")
close_loop=False
game_over1=False
while not game_over1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                    print("QUIT GAME")
                    pygame.quit()
                    sys.exit()
        while True:
            try:
                
                # カメラからの画像取得
                ret, frame = cap.read()
                # カメラの画像から手を検出
                image = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
                results = hands.process(image)
                mark_list = []
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        for i in range(21):
                            x = hand_landmarks.landmark[i].x

                            y = hand_landmarks.landmark[i].y
                            z = hand_landmarks.landmark[i].z
                            # print("x:",int(x*700))
                            # print("y:",int(y*700))

                            mark_list.append(x)
                            mark_list.append(y)
                            mark_list.append(z)
                            if results.multi_hand_landmarks:
                                pygame.draw.rect(
                                    screen, GRAY, (0, 0, width, squaresize)
                                )
                                if int(x * 699) <= 0:
                                    posx = 0
                                elif int(x * 699) < 699:
                                    posx = int(x * 699)
                                else:
                                    posx = 699

                                if turn == 0:
                                    pygame.draw.circle(
                                        screen, RED, (posx, int(squaresize / 2)), radius
                                    )
                                else:
                                    pygame.draw.circle(
                                        screen,
                                        YELLOW,
                                        (posx, int(squaresize / 2)),
                                        radius,
                                    )


                    mark_list = np.array(mark_list)
                    # print(mark_list)

                    # ロジスティック回帰モデルを使ってじゃんけんの手を予測
                    # mark_listが空だとValueErrorになってtryから脱出
                    pred = model.predict(mark_list.reshape(1, -1))
                    print(pred[0])
                    # print("Test set score: {:.2f}".format(np.mean(pred == Y_test)))
                    # 描き
                    cv2.putText(
                        frame,
                        text=str(pred[0]),
                        org=(0, 50),
                        fontFace=cv2.FONT_HERSHEY_TRIPLEX,
                        fontScale=1.0,
                        color=(0, 255, 0),
                        thickness=2,
                        lineType=cv2.LINE_4,
                    )
                    # カメラの画像の出力(windows)
                    cv2.imshow("camera", frame)

                    ###########AI###########
                    ########################
                    print("x:", int(x * 699))
                    pygame.display.update()
                    if str(pred[0]) == "catch_coin":
                        print("append")
                        # print(command_list)
                        command_list[1] = "catch"
                    elif str(pred[0]) == "put_coin":
                        # print(command_list)
                        # if results.multi_hand_landmarks and str(pred[0]) == "put_coin":
                        # elif command_list[-1] == "catch" and str(pred[0]) == "put_coin":
                        if command_list[1] == "catch":
                            pygame.draw.rect(screen, GRAY, (0, 0, width, squaresize))
                            # print("左クリックした座標:"+str(event.pos))
                            # player 1 input
                            # 正規化された座標を変換して、boardの大きさの制限を設定
                            if turn == 0:
                                chek_board[0] = board.tolist()
                                if int(x * 699) <= 0:
                                    posx = 0
                                elif int(x * 699) < 699:
                                    posx = int(x * 699)
                                else:
                                    posx = 699
                                col = int(math.floor(posx / squaresize))
                                print(col)

                                # col = int(input("Player 1 Make your selection (0-6):") )
                                if is_volid_loction(board, col):
                                    row = get_next_open_row(board, col)
                                    drop_piece(board, row, col, 1)
                                    draw_board(board)
                                    # 勝利判断
                                    if winning_move(board, 1):
                                        player_1_win = "Player1 WIN"
                                        print(player_1_win + "!!!")
                                        label = sysfont.render(player_1_win, 1, RED)
                                        screen.blit(label, (40, 10))
                                        pygame.display.update()

                                        speach(player_1_win)
                                        game_over = True
                                time.sleep(1)

                            # player 2 input
                            else:
                                chek_board[0] = board.tolist()
                                # 正規化された座標を変換して、boardの大きさの制限を設定
                                if int(x * 699) <= 0:
                                    posx = 0
                                elif int(x * 699) < 699:
                                    posx = int(x * 699)
                                else:
                                    posx = 699
                                col = int(math.floor(posx / squaresize))
                                print(col)
                                # col = int(input("Player 2 Make your selection (0-6):") )
                                if is_volid_loction(board, col):
                                    row = get_next_open_row(board, col)

                                    drop_piece(board, row, col, 2)
                                    draw_board(board)
                                    # 勝利判断
                                    if winning_move(board, 2):
                                        player_2_win = "Player2 WIN"
                                        print(player_2_win + "!!!")
                                        label = sysfont.render(player_2_win, 1, YELLOW)
                                        screen.blit(label, (40, 10))
                                        pygame.display.update()
                                        speach(player_2_win)
                                        game_over = True
                                time.sleep(1)

                            print_board(board)
                            chek_board[1] = board.tolist()
                            if chek_board[0] == chek_board[-1]:
                                continue
                            else:
                                turn += 1
                                turn = turn % 2
                                command_list[1] = "put_coin"
                                print(board[0])

                            # turn += 1
                            # turn = turn % 2

                        # elif str(pred[0]) == "catch_coin":
                        ###################
                        #######AI＿END############
                        ####################
                        """
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            pygame.draw.rect(screen, GRAY, (0, 0, width, squaresize))
                            print("左クリックした座標:" + str(event.pos))
                            # player 1 input
                            if turn == 0:
                                posx = event.pos[0]
                                col = int(math.floor(posx / squaresize))

                                # col = int(input("Player 1 Make your selection (0-6):") )
                                if is_volid_loction(board, col):
                                    row = get_next_open_row(board, col)
                                    drop_piece(board, row, col, 1)
                                    draw_board(board)
                                    #勝利判断
                                    if winning_move(board, 1):
                                        player_1_win = "Player1 WIN"
                                        print(player_1_win + "!!!")
                                        label = sysfont.render(player_1_win, 1, RED)
                                        screen.blit(label, (40, 10))
                                        pygame.display.update()
                                        #音声関数でplayer_1_winを読み上げ
                                        speach(player_1_win)
                                        game_over = True
                            # player 2 input
                            else:
                                posx = event.pos[0]
                                col = int(math.floor(posx / squaresize))

                                # col = int(input("Player 2 Make your selection (0-6):") )
                                if is_volid_loction(board, col):
                                    row = get_next_open_row(board, col)
                                    drop_piece(board, row, col, 2)
                                    draw_board(board)
                                    
                                    #勝利判断
                                    if winning_move(board, 2):
                                        player_2_win = "Player2 WIN"
                                        print(player_2_win + "!!!")
                                        label = sysfont.render(player_2_win, 1, YELLOW)
                                        screen.blit(label, (40, 10))
                                        pygame.display.update()
                                        #音声関数でplayer_1_winを読み上げ
                                        speach(player_2_win)
                                        game_over = True
                            #boardの情報をprint
                            print_board(board)
                            #先手が終わった後の順番の仕組み
                            turn += 1
                            turn = turn % 2
                        """
                    if game_over:
                        save_time = t
                        print(t)
                        # t = 10
                        while t > 0:
                            pygame.draw.rect(screen, GRAY, (0, 0, width, squaresize))
                            # print(t)

                            label = sysfont.render(f"{t}sec RESET", 1, BLACK)
                            screen.blit(label, (40, 10))
                            pygame.display.update()
                            time.sleep(1)
                            t -= 1
                        time.sleep(1)
                        t = save_time
                        # pygame.time.wait(5000)
                        # 一秒後restart game over false loop続く
                        game_over = False
                        # turn はrestart後の先手、後手の設定
                        turn = 0
                        # boardをreset
                        board = creat_board()
                        print(board)
                        draw_board(board)
                        # 画面情報GUIを更新
                        pygame.display.update()

                    # print(user_choice)
                    # 座標list
                    # print(mark_list)
                    # 繰り返し分から抜けるためのif文
                key = cv2.waitKey(10)
                if key == 27 :
                    print("close game")
                    game_over1=True
                    break
                               

            except ValueError:
                pass

# メモリを解放して終了するためのコマンド
cap.release()
cv2.destroyAllWindows()
