# Importing Libraries 
import cv2 
import mediapipe as mp 
from math import hypot 
import screen_brightness_control as sbc 
import numpy as np 
import HandTrackingModule as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import keyboard
import time
import speech_recognition as sr
# Initializing the Model 
mpHands = mp.solutions.hands 
hands = mpHands.Hands( 
	static_image_mode=False, 
	model_complexity=1, 
	min_detection_confidence=0.75, 
	min_tracking_confidence=0.75, 
	max_num_hands=2) 
Draw = mp.solutions.drawing_utils 
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume.iid, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
# Start capturing video from webcam 
def press_windows_m():
    # Simulate pressing Windows key
    keyboard.press("windows")
    keyboard.press_and_release("m")
    keyboard.release("windows")
def press_windows_M():
    # Simulate pressing Windows key
    keyboard.press("windows")
    keyboard.press("shift")
    keyboard.press_and_release("m")
    keyboard.release("windows")
    keyboard.release("shift")
def press_windows_deskr():
    # Simulate pressing Windows key
    keyboard.press("windows")
    keyboard.press("ctrl")
    keyboard.press_and_release("right")
    keyboard.release("windows")
    keyboard.release("ctrl")
def press_windows_deskl():
    # Simulate pressing Windows key
    keyboard.press("windows")
    keyboard.press("ctrl")
    keyboard.press_and_release("left")
    keyboard.release("windows")
    keyboard.release("ctrl")
def press_windows_windc():
    # Simulate pressing Windows key
    keyboard.press("alt")
    keyboard.press("esc")
    keyboard.release("alt")                 
    keyboard.release("esc")
def press_windows_tabc():
    # Simulate pressing Windows key
    keyboard.press("ctrl")
    keyboard.press("tab")
    keyboard.release("ctrl")                 
    keyboard.release("tab")
def press_windows_windcp():
	# Simulate pressing Windows key
    keyboard.press("alt")
    keyboard.press("shift")
    keyboard.press_and_release("esc")
    keyboard.release("alt")
    keyboard.release("shift") 
def press_windows_tabcp():
    # Simulate pressing Windows key
    keyboard.press("ctrl")
    keyboard.press("shift")
    keyboard.press("tab")
    keyboard.release("ctrl")
    keyboard.release("shift")                 
    keyboard.release("tab")
def press_windows_browser():
    # Simulate pressing Windows key
    keyboard.press("windows")
    keyboard.press_and_release("6")
    keyboard.release("windows")
recognizer = sr.Recognizer()
def capture_voice_input():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    return audio    
def convert_voice_to_text(audio):
    try:
        text = recognizer.recognize_google(audio)
        print("You said: " + text)
    except sr.UnknownValueError:
        text = ""
        print("Sorry, I didn't understand that.")
    except sr.RequestError as e:
        text = ""
        print("Error; {0}".format(e))
    return text
def process_voice_command(text):
    if "hello" in text.lower():
        print("Hello! How can I help you?")
    elif "goodbye" in text.lower():
        print("Goodbye! Have a great day!")
        return True
    else:
        print("I didn't understand that command. Please try again.")
    return False
def vinp():
    end_program = False
    while not end_program:
        audio = capture_voice_input()
        text = convert_voice_to_text(audio)
        end_program = process_voice_command(text)

if _name_ == "_main_":
      cap = cv2.VideoCapture(0) 

while True: 
	# Read video frame by frame 
	_, frame = cap.read() 

	# Flip image 
	frame = cv2.flip(frame, 1) 

	# Convert BGR image to RGB image 
	frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 

	# Process the RGB image 
	Process = hands.process(frameRGB) 

	landmarkList = [] 
	# if hands are present in image(frame) 
	if Process.multi_hand_landmarks:
		 
		# detect handmarks 
		for handlm in Process.multi_hand_landmarks: 
			for _id, landmarks in enumerate(handlm.landmark): 
				# store height and width of image 
				height, width, color_channels = frame.shape 

				# calculate and append x, y coordinates 
				# of handmarks from image(frame) to lmList 
				x, y = int(landmarks.x*width), int(landmarks.y*height) 
				landmarkList.append([_id, x, y])
				handedness = Process.multi_handedness[0].classification[0].label

			# draw Landmarks 
			Draw.draw_landmarks(frame, handlm, 
								mpHands.HAND_CONNECTIONS) 
			cv2.putText(frame, handedness, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

	# If landmarks list is not empty 
          
	if landmarkList != []:
		if handedness == "Left":
		 		# store x,y coordinates of (tip of) thumb 
			x_7, y_7 = landmarkList[4][1], landmarkList[4][2] 
			x_8, y_8 = landmarkList[12][1], landmarkList[12][2] 
			x_9, y_9 = landmarkList[8][1], landmarkList[8][2]
            
			cv2.circle(frame, (x_7, y_7), 7, (0, 255, 0), cv2.FILLED) 
			cv2.circle(frame, (x_8, y_8), 7, (0, 255, 0), cv2.FILLED)
			cv2.circle(frame, (x_9, y_9), 7, (0, 255, 0), cv2.FILLED)
			cv2.line(frame, (x_7, y_7), (x_8, y_8), (0, 255, 0), 3)
			cv2.line(frame, (x_7, y_7), (x_9, y_9), (0, 255, 0), 3)
			L = hypot(x_8-x_7, y_8-y_7)
			VL = hypot(x_9-x_7, y_9-y_7)
        
			b_level = np.interp(L, [15, 220], [0, 100]) 
			sbc.set_brightness(int(b_level))
			v_level = np.interp(VL , [50, 200], [-45.25, 0.0]) 
			volume.SetMasterVolumeLevel(v_level,None)
		if handedness == "Right":
		 		# store x,y coordinates of (tip of) thumb 
			x_1, y_1 = landmarkList[4][1], landmarkList[4][2] 
			x_2, y_2 = landmarkList[8][1], landmarkList[8][2]
			x_3, y_3 = landmarkList[12][1], landmarkList[12][2]
			x_4, y_4 = landmarkList[16][1], landmarkList[16][2] 
			x_5, y_5 = landmarkList[20][1], landmarkList[20][2]
			cv2.circle(frame, (x_1, y_1), 7, (0, 255, 0), cv2.FILLED)
			cv2.circle(frame, (x_2, y_2), 7, (0, 255, 0), cv2.FILLED)
			cv2.circle(frame, (x_3, y_3), 7, (0, 255, 0), cv2.FILLED)
			cv2.circle(frame, (x_4, y_4), 7, (0, 255, 0), cv2.FILLED) 
			cv2.circle(frame, (x_5, y_5), 7, (0, 255, 0), cv2.FILLED)
			cv2.line(frame, (x_1, y_1), (x_5, y_5), (0, 255, 0), 3)
			cv2.line(frame, (x_1, y_1), (x_4, y_4), (0, 255, 0), 3)
			cv2.line(frame, (x_1, y_1), (x_2, y_2), (0, 255, 0), 3) 
			cv2.line(frame, (x_1, y_1), (x_3, y_3), (0, 255, 0), 3)
			a = hypot(x_2-x_1, y_2-y_1)
			b = hypot(x_3-x_1, y_3-y_1) 
			c = hypot(x_4-x_1, y_4-y_1)
			d = hypot(x_5-x_1, y_5-y_1) 
 
			if a >= 100 and b <100:
				press_windows_m()
				time.sleep(1)
			if b >= 100:
				press_windows_M()
				time.sleep(1)
			if c >= 70 and d <50 and b< 50:
				press_windows_deskl()
				time.sleep(1)
			if d >= 100 and c<80:
				press_windows_deskr()
				time.sleep(1)
			if a >= 100 and b>=100 and c<50:
				press_windows_windc()
				time.sleep(1)
			if c >= 80 and d>=70 and b<50:
				press_windows_tabc()
				time.sleep(1)
			if a >= 100 and b>=100 and c>=80 and d< 50:
				press_windows_windcp()
				time.sleep(1)
			if c >= 80 and d>=70 and b>=100 and a <50:
				press_windows_tabcp()
			if a >= 100 and b>=100 and c>=80 and d> 50:
				press_windows_browser()
                
				time.sleep(1)
                        
				
			
			 
 
	cv2.imshow('Image', frame) 
	if cv2.waitKey(1) & 0xff == ord('q'): 
		break