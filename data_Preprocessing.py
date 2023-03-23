import os
import glob
import cv2
import pandas as pd
import mediapipe as mp
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pickle
import random
df = []
for foldername in os.listdir('./fou_coin/photo_train/'):
    imgs_path = './fou_coin/photo_train/' + foldername
    imgs = sorted(glob.glob(imgs_path + '/' + '*.jpg'))
    for name in imgs:
        df.append((str(name), str(foldername)))
df = pd.DataFrame(df, columns=['img', 'label'])
print(df.head())

#検出器のインスタンス化 defult is 0.5 min_detection_confidence=0.5
hands = mp.solutions.hands.Hands(static_image_mode=True,  min_detection_confidence=0.6)
#静止画モードmax_num_hands=1, #検出する手の数(じゃんけんは片手の想定なので1に)

df1 = []
for idx, file in enumerate(df['img']):
    #print('No', idx)
    #画像を読み込んで左右反転させる
    image = cv2.flip(cv2.imread(file), 1)
    #色をRGBにして手の検出を行う
    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    #手が検出されなければ次の画像へ
    if not results.multi_hand_landmarks:
        print('No', idx)
        print('No Hand')
        #print('-------------------------')
        continue
    mark_list = []
    #21個の検出ポイントを取得
    for i in range(21):
        x = results.multi_hand_landmarks[0].landmark[i].x
        y = results.multi_hand_landmarks[0].landmark[i].y
        z = results.multi_hand_landmarks[0].landmark[i].z
        mark_list.append(x)
        mark_list.append(y)
        mark_list.append(z)
    #手のラベルと合わせてdf1に保存
    mark_list.append(df['label'][idx])
    df1.append(mark_list)
    #rint(complete)
    #print('-------------------------')
df1 = pd.DataFrame(df1)
print(df1.shape)#---> (5880, 64)

df2 = []
for idx, file in enumerate(df['img']):
    #print('No', idx)
    image = cv2.imread(file, 1) #flipしない→逆の手としてデータとれるはず
    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    if not results.multi_hand_landmarks:
        print('No', idx)
        print('No Hand')
        #print('-------------------------')
        continue
    mark_list = []
    for i in range(21):
        x = results.multi_hand_landmarks[0].landmark[i].x
        y = results.multi_hand_landmarks[0].landmark[i].y
        z = results.multi_hand_landmarks[0].landmark[i].z
        mark_list.append(x)
        mark_list.append(y)
        mark_list.append(z)
    mark_list.append(df['label'][idx])
    df2.append(mark_list)
    #print('-------------------------')

df2 = pd.DataFrame(df2)
print(df2.shape)#---> (5858, 64)

df3 = pd.concat([df1, df2])
print(df3.shape)#---> (1195, 64)
print(df3.head())
df3.to_csv('./fou_coin/landmarkdata.csv', index=False)
