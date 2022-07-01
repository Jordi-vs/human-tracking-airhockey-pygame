# About the Game
This is an Air Hockey game (just like at the arcades) where 2 players play against each other and try to get the "ball" into the goal on their opponents side. This version of the game translates a persons position in real life into the game using a camera and the OpenCV library. The game is intended to be played using 2 cameras on 1 computer, however a simplified single player version is also possible utilizing the mouse. The game was made with the intention of being used by Team Epoch at TU Delft for demonstration purposes at events.

# How to play
To start playing, ensure you have python installed, and then:
- Navigate to the "human-tracking-airhockey-pygame" directory
- Run pip install -r requirements.txt
- Run python AirHockey.py

If both cameras are plugged in and functioning, it should launch the game and allow you to play as intended.

If you would like to try the single player you will need to uncomment one piece of code and comment another. Navigate to the AirHockey.py file and starting from line 145 you will find this code block.
![](https://i.imgur.com/2OnXISI.png)
This will enable the 2 camera functionality. If you want to try out the single player with the mouse simply comment out both `image_to_player_pos(p1)` and `image_to_player_pos(p2)` and uncomment `mouse_to_player_pos()`.

# Future Improvements
1. Currently everything is run on 1 computer and requiring 2 cameras, which can be awkward to set up. Introducing an online alternative will reduce both the load on the computer and allow for an easier camera setup.
2. Currently the ball will shoot into a random direction when touched and slowly accelerate over time. There is no proper functioning physics model that can calculate the angle nor the speed at which it should go if hit harder.
3. There is a bug that occurs from time to time where the ball gets stuck on the edge and jitters back and forth.
4. Overall art. Although not awful, images are stretched and not appropriately created. The art is also not consistent with each other.

# Finally
Thank you for reading! For any questions feel free to contact me on Jordivpsn@gmail.com. Have fun!

