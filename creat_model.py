import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pickle
#作成したcsvファイルの読み込み
df = pd.read_csv('./fou_coin/landmarkdata.csv')

#特徴量列とラベル列に分離
X = df.drop('63', axis=1)
y = df['63']

#クラスラベルの数値化。変換の対応を確認したいので変換前後で表示しておく
#print(y[0], y[300], y[590])
#---> choki  gu  pa
#le = LabelEncoder()
#y = le.fit_transform(y)
#print(y[0], y[300], y[590])
#---> 0  1  2
#訓練データとテストデータに分割

#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

#ロジスティック回帰モデルで学習を行い、テストデータのスコアを表示
#lr = LogisticRegression()
#lr.fit(X_train, y_train)
#print(lr.predict(X_test))
#print(lr.score(X_test, y_test))
#ランダムフォレスト
from sklearn.ensemble import RandomForestClassifier
#回帰の場合は　RandomForestRegressor　を使う
from sklearn.model_selection import train_test_split
#警告非表示
import warnings
warnings.simplefilter('ignore')

#データ分割
X_train,X_test,Y_train,Y_test = train_test_split(X,y,random_state=42)
#インスタンス作成
#n_estimators　木の数
#max_depth　木の深さ
#max_features　使用する特徴量
forest = RandomForestClassifier(n_estimators=15)
#学習
forest.fit(X_train, Y_train)
#予測
pred = forest.predict(X_test)
print("Y_test:",*Y_test)
print("pred:",*pred)
print("Test set score: {:.2f}".format(np.mean(pred == Y_test)))
#0.99 (精度)
"""
a = X_test.iloc[0, :]
test = np.array([a[i] for i in range(len(a))])
pred = forest.predict(test.reshape(1, -1))
prob = forest.predict_proba(test.reshape(1, -1))[0][pred[0]]
"""
with open('./fou_coin/model/logistic.pkl', 'wb') as f:
    pickle.dump(forest, f)

