#magic_game_PJ
import os
import glob
import cv2
import pandas as pd
import mediapipe as mp
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pickle
import random

#後で使う対応表の作成
#label_dict = {0: 'b', 1: 'a', 2: 'c'}
#dic = {"a": "wait_magic", "b": "magic_attack", "c": "magic_defense"}

#前工程で作ったモデルの取得

with open('./fou_coin/model/logistic.pkl', 'rb') as f:
    model = pickle.load(f)
    
    #検出器のインスタンス化
hands = mp.solutions.hands.Hands(static_image_mode=True,max_num_hands=1,min_detection_confidence=0.5)
cap = cv2.VideoCapture(0)

########################################################################################################
########################################################################################################
#繰り返しのためのwhile文
while True:
    try:
        #カメラからの画像取得
        ret, frame = cap.read()
        #カメラの画像から手を検出
        image = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
        results = hands.process(image)
        mark_list = []
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for i in range(21):
                    x = hand_landmarks.landmark[i].x
                    
                    y = hand_landmarks.landmark[i].y
                    z = hand_landmarks.landmark[i].z
                    print("z:",int(x*700))
                    #print("y:",int(y*700))  
                    
                    mark_list.append(x)
                    mark_list.append(y)
                    mark_list.append(z)
        mark_list = np.array(mark_list)
        #print(mark_list)
        
        
        #ロジスティック回帰モデルを使ってじゃんけんの手を予測
        #mark_listが空だとValueErrorになってtryから脱出
        pred = model.predict(mark_list.reshape(1, -1))
        print(pred[0])
        #print("Test set score: {:.2f}".format(np.mean(pred == Y_test)))

        """
        prob = model.predict_proba(mark_list.reshape(1, -1))[0][pred[0]]
        print(pred)
        
        user = label_dict[pred[0]]
        user_choice = dic[user]
        """
        
        #描き        
        cv2.putText(frame,text=str(pred[0]),org=(0, 50),fontFace=cv2.FONT_HERSHEY_TRIPLEX,fontScale=1.0,color=(0, 255, 0),thickness=2,lineType=cv2.LINE_4)
        
        """
        cv2.putText(frame,text=str(int(prob*100))+"%",org=(0, 100),fontFace=cv2.FONT_HERSHEY_TRIPLEX,fontScale=1.0,color=(0, 255, 0),thickness=2,lineType=cv2.LINE_4)
        
        cv2.putText(img_choki,text="AI",org=(0, 30),fontFace=cv2.FONT_HERSHEY_TRIPLEX,fontScale=1.0,color=(0, 255, 0),thickness=2,lineType=cv2.LINE_4)
        cv2.putText(img_pa,text="AI",org=(0, 30),fontFace=cv2.FONT_HERSHEY_TRIPLEX,fontScale=1.0,color=(0, 255, 0),thickness=2,lineType=cv2.LINE_4)
        cv2.putText(img_gu,text="AI",org=(0, 30),fontFace=cv2.FONT_HERSHEY_TRIPLEX,fontScale=1.0,color=(0, 255, 0),thickness=2,lineType=cv2.LINE_4)

        cv2.putText(user_img_choki,text="USER",org=(0, 30),fontFace=cv2.FONT_HERSHEY_TRIPLEX,fontScale=1.0,color=(0, 255, 0),thickness=2,lineType=cv2.LINE_4)
        cv2.putText(user_img_pa,text="USER",org=(0, 30),fontFace=cv2.FONT_HERSHEY_TRIPLEX,fontScale=1.0,color=(0, 255, 0),thickness=2,lineType=cv2.LINE_4)
        cv2.putText(user_img_gu,text="USER",org=(0, 30),fontFace=cv2.FONT_HERSHEY_TRIPLEX,fontScale=1.0,color=(0, 255, 0),thickness=2,lineType=cv2.LINE_4)
        
        #catImg2 = cv2.imread("./cat2.jpg")
        if user_choice =="Paper":
            cv2.imshow('AI_choki' , img_choki)
            cv2.imshow('USER' , user_img_pa)
        elif user_choice =="Rock":
            cv2.imshow('AI_choki' , img_pa)
            cv2.imshow('USER' , user_img_gu)
        elif user_choice =="Scissors":
            cv2.imshow('AI_choki' , img_gu)
            cv2.imshow('USER' , user_img_choki)
        #mergeImg = np.hstack((frame, catImg1))
        
        #test1 = cv2.imread("C:/Users/GOD/Desktop/OLD_PC/日本工学院/WEB開発実習/じゃんけん/img_janken/janken_choki.png")
        """
           
        #カメラの画像の出力(windows)
        cv2.imshow('camera' , frame)
          
        #print(user_choice)
            
        
        #座標list
        #print(mark_list)

        #繰り返し分から抜けるためのif文
        
        key =cv2.waitKey(10)
        if key == 27:
            break
    except ValueError :
        pass

#メモリを解放して終了するためのコマンド
cap.release()
cv2.destroyAllWindows()

########################################################################################################
########################################################################################################
