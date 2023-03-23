# four_conect_game_handAI
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

#Important: The prerequisite is that MediaPipe pygame gTTS scikit-learn opencv has been installed. 
If you want to train the module from scratch, the sequence of execution files is data_Preprocessing.py→creat_model.py→main01.py and the end method is ctrl+c or press esc on the camera screen.  
hand_put_coin_ai.py simply uses webcamera and distinguishes and displays AI prediction results. 
To end main.py, please use Ctrl+c to end the program.
