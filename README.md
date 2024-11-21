
> [!WARNING]
> when uae my model can not work on python 3.12
> scikit == 1.2.0
> python3.10

# four_conect_game_handAI
example video link1:https://youtu.be/lED6AqMGo1Y
example video link1:https://youtu.be/5kvjuJ-v3p4
Hand sorting process.  Use MediaPipe to get hand coordinates and generate a new dataset (csv file).
Then use Landam Forest to store the model after the classification learning is completed. This model will be stored in the model folder. 
main.py is the version of four connect that only uses the mouse to move the coin and click it, which is the prototype.
Regardless of whether main.py or main01.py is used at the beginning, gTTS will make a sound to inform the game to start.
After reading, the user will be asked to input the waiting time for rereading (reset) when any one of player1 or player2 loses.
Pressing enter will start the game (using pygame).  main01.py has the models imported to learn. 
As mentioned above, the opening screen is the same. When enter is pressed, the pygame game screen will pop up.
At this time, the webcamera needs to be connected, and the coin will also move when the hand is moved in front of the camera.
When releasing the coin action, the coin will be put down and wait for player2's hand operation.
Since the model has been uploaded, if you want to train the model yourself.  You can put photos in photo_train/.
There are two file folders put_coin and catch_coin in photo_train. Store the photos of catching coins that you want to learn into this file folder.
put_coin is a picture of the action of putting down the coin.  Since I had more photos of myself when I was studying, I only uploaded a sample photo.
I took 500 of each during training.  If you don't want to train the model, you can start main01.py directly.

Important: The prerequisite is that MediaPipe pygame gTTS scikit-learn opencv has been installed. 

If you want to train the module from scratch, the sequence of execution files is data_Preprocessing.py→creat_model.py→main01.py and the end method is ctrl+c or press esc on the camera screen.  
hand_put_coin_ai.py simply uses webcamera and distinguishes and displays AI prediction results. 
To end main.py, please use Ctrl+c to end the program.

These programs can all be executed on the pc jetson nano.  PC can directly use the pip3 install MediaPipe installation method.  Please follow this process to install jetson nano https://google.github.io/mediapipe/getting_started/python.html
gTTS install command:pip3 install gTTS
pygame install command:pip3 install pygame
when use jetson nano main01.py line192: main.py line183:set sysfont = pygame.font.SysFont(None, 75)

手の認識の流れ。
MediaPipe を使用して手の座標を取得し、新しいデータセット (csv ファイル) を生成します。 
分類学習が完了したら、Landam Forest を使用してモデルを保存します (このモデルはモデル フォルダーに保存されます)。 
main.py は、プロトタイプであるコインの移動とクリックにマウスのみを使用するバージョンの four connect です。
最初に main.py と main01.py のどちらを使用しても、gTTS が音を出してゲームの開始を知らせます。
読み込み後、player1 または player2 のいずれかが負けた場合、再読み込み (リセット) の待ち時間を入力するように求められます。
Enter キーを押すと、ゲームが開始されます (pygame を使用)。  main01.py には、学習するためにインポートされたモデルがあります。
オープニング画面は先ほどと同じで、エンターを押すとpygameのゲーム画面がポップアップします。
このとき、webcameraを接続する必要があり、カメラの前で手を動かすとコインも動きます。 コインアクションをリリースすると、コインが置かれ、プレイヤー2の手の操作を待ちます。
モデルがアップロードされているので、自分でモデルをトレーニングしたい場合。 
photo_train/ に写真を入れることができます。
photo_train には put_coin と catch_coin の 2 つのファイル フォルダーがあり、学習したいキャッチ コインの写真をこのファイル フォルダーに格納します。  
put_coin は、コインを置くアクションの画像です。 
train中の自分の写真が多かったので、サンプル写真だけアップしました。 私はトレーニング中にそれぞれ500個取りました。
モデルをトレーニングしたくない場合は、main01.py を直接開始できます。 

重要: 前提条件は、MediaPipe pygame gTTS scikit-learn opencv がインストールされていることです。 
モジュールをゼロからトレーニングする場合、実行ファイルの順序は data_Preprocessing.py → creat_model.py → main01.py で、終了方法は ctrl+c またはカメラ画面で esc を押します。 
hand_put_coin_ai.py は単純にwebcameraを利用し、AI の予測結果を判別して表示します。  main.py を終了するには、Ctrl+c を使用してプログラムを終了してください。

これらのプログラムはすべて、PC 或いはjetson nanoで実行できます。 
PC は pip3 install MediaPipe インストール方法を直接使用できます。 
jetson nanoの場合は公式に従ってインストールしてください https://google.github.io/mediapipe/getting_started/python.html
gTTSをインストールpip3 install gTTS
pygameをインストールpip3 install pygame
jetson nano の時 main01.py line192: main.py line183:set sysfont = pygame.font.SysFont(None, 75)

手部分類的流程。利用MediaPipe取得手部座標並產生新的dataset (csv file)。
再利用 Landam Forest 的分類學習完成後儲存模型此模型會存放在model檔案夾裡面。
main .py是four connect 的只利用滑鼠移動硬幣以及點擊時會動作的版本也就是原型。
無論啟動main.py還是main01.py最一開始利用了gTTS會發出聲音告知一開始遊戲。
念完後會請使用者輸入player1或player2任一者輸的時候重新再來一次的重讀（reset)的等待時間。
按下enter後會開始遊戲（使用pygame)。main01.py 有導入以學習的模型。
如前面所提到的開啟時的畫面也一樣，當enter按下後會跳出pygame的遊戲畫面。此時需要已連結webcamera ，把手放在相機前移動時硬幣也會跟著移動。當放開硬幣的動作時硬幣會放下及等待player2的手的操作。
由於已經上傳了模型 如果想要自己訓練模型。可以放照片在photo_train/裡面。photo_train裡面有兩個檔案夾put_coin和catch_coin將想要學習的抓取硬幣的照片存入此檔案夾裡。
put_coin則是放下硬幣的動作的照片。由於我在學習時有本人的照片居多於事我只上傳個一張範例照片。
在訓練時我各拍了個500張。如果不想要訓練模型的話可以直接啟動main01.py。重要：前提是要已安裝MediaPipe pygame gTTS scikit-learn opencv。
要從頭開始訓練模組的話執行檔案的順序為data_Preprocessing.py→creat_model.py→main01.py
結束方法為ctrl+c 或者是在相機的畫面按下esc。
hand_put_coin_ai.py 則是單純使用webcamera 並辨別顯示AI的預測結果。main.py的結束方法請利用Ctrl+c結束程式。

這些程式皆可在pc jetson nano上執行 。pc 可以直接利用 pip3 install MediaPipe 安裝方式。jetson nano請按照此流程安裝https://google.github.io/mediapipe/getting_started/python.html
gTTS 安裝指令 pip3 install gTTS
pygame 安裝指令 pip3 install pygame
jetson nano main01.py line192: main.py line183:set sysfont = pygame.font.SysFont(None, 75)
