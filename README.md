# simple_talking_robot
A very simple talking robot head code for rasbperry pi
- python2.7.*
Check Setup.txt to get started.

- This project currently implements a bisc robot head which is desinged using raspberry pi boards.
- It handles pre-defined conversation (without any nlp), face recognition and head pan/tilt.

-The robot starts a conversation and simultaneously, starts moving the head around to find familiar faces. If one found, it tries to follow the face as they move around. 
It also starts using the name of the found face while still in sight.
- In order to get it familiarized with your face, train opencv face recognition and export it. Then you could load the XML by uncommenting and editing the line (#recognizer.load(os.path.join(current_dir, 'trained_model.xml'))) in camera.py

- My hardware setup for this code is a pair of Raspberry-pi 3 boards:
	#1: Handles the neck and sight control. It is connected to a pi-camera. There is a servo-pi board connected to the board which controls two servo motors connected through a pan/tilt bracket.
	#2: Handles the speaking. It is connected to a speaker, and through a USB soundcard to a microhpne.
	(I connected the 2 pi boards through a LAN cable, you could use 1, I extended to a second board to allocated a full board to image recognition.)

- start_head.py and start_speech.py shall be executed separately to start the robot. Once they manage to hand-shake, they start communicating through the socket.

Speech engine operates better connected to the internet, but it continues working if internet connection is lost:
- Speech to Text is implemented using speech_recognition package which uses Google API if the device is connected to the internet, and the backup is sphinx if the device had no internet connection.
- Text to Speech is implemented using Amazon IVONA API, and the backup is pyttsx if the device has no internet connection.


