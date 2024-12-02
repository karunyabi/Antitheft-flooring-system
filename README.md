for installing all modules, either install from requirements.txt file (pip install -r requirements.txt) or just run the command below: 
`pip install flask numpy opencv-python face-recognition pygame pyserial`

mostly you will get error while trying to install face_recognition module... if you get any error call

Steps:
1. change the path for "buzzer.wav" file to the one you are using in your laptop or whatever
2. first run that app.py
3. register face
4. terminate the program
5. then run main.py
6. i will put that pin diagram and photos in wiring folder
7. for now use my mail ID for smtp mailing (alert mailing) itself.. you have to setup app password and all separately if you have to use your mail
8. tap on the piezo.. it should say pressure detected and video will start capturing.. if face registered there wont be any alert sent
9. if unkown face is there or no face is there, then loud buzzer will start playing and there will be a popup for secret code that you have to enter to disable the alarm which is "1234" for now, you can change that as whatever password you want and can use letters also.
10. dont forget to terminate the program after using
11. any doubts call me
12. dont die, if you say shit like you deserve to die or something i will come and slap you



Future Scope:

You can include heavy duty platform scales to place on top of durable spring mounted on the piezo to activate it and can use multiple piezos
esp's webserver can be utilised for logging in to it's network to disable alarm (using keypad matrix) or modify and add new faces for added security (advanced iot based security system)
