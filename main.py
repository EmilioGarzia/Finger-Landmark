# Finger Landmark
#
# @description Using openCV and Mediapipe to mark only specifics finger on the hand.
#              In this source code you can find also a function to compute the distance between two fingers and also if them touch.
#              In this source code you can find also a function that return if the subject show the left or right hand
#
# @author Emilio Garzia

import cv2 as cv
import mediapipe as mp
import math
import pyautogui as pg
import modules.colours as colours
from modules.fingers import FINGER_LIST
import pyautogui
import argparse as ap

# Argument parser
parser = ap.ArgumentParser()
parser.add_argument("-H", "--hand", default="r", help="'l' for left hand, 'r' for right hand", choices=["l","r"])
parser.add_argument("-n", "--nodebug", action="store_true", default=False, help="Show/Hide the camera window debug")
args = vars(parser.parse_args())

choosed_hand = args["hand"]

# This function return x,y coordinates of the specified finger points
def coordinates_of(finger, frame):
    img_height, img_width, _ = frame.shape
    index_finger = hand_landmarks.landmark[finger]
    cx, cy = int(index_finger.x * img_width), int(index_finger.y * img_height)
    return cx, cy, index_finger

# This function compute the distance between two fingers
def distance_between(point1, point2):
    return math.sqrt((point1.x-point2.x)**2 + (point1.y-point2.y)**2)*100  # 100 is the bias

# This function check if two fingers are touched
def is_touched(finger1, finger2, threshold):
    distance = distance_between(finger1, finger2)
    if distance < threshold:
        return True
    return False

# Function that return if the hands is the left or right
def is_left_or_right(threshold):
    wrist_x = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x
    if wrist_x > threshold:
        return "l"
    else:
        return "r"

# Draw a circle around the finger point
def mark_finger(frame, finger_point, color=(255,0,0)):
    X, Y, index = coordinates_of(FINGER_LIST[finger_point], frame)
    cv.circle(frame, (X,Y), 10, color, cv.FILLED)
    return X, Y, index

# Check if the gesture is a fist
def is_fist(thumb, index, middle, ring, pinky):
    if is_touched(index, middle, 5) and is_touched(middle, ring, 5) and is_touched(ring, pinky, 5):
        return True
    return False

# Open the stream with main camera
camera = cv.VideoCapture(0)

# Initialize the Hands object
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Start the capturing
while True:
    ret, frame = camera.read()

    if not ret:
        break

    image_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    # Draw circles on the left hand at specific fingers
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            if is_left_or_right(0.5) == choosed_hand:    
                thumbX, thumbY, thumb_index = mark_finger(frame=frame, finger_point=4, color=colours.RED)  
                indexX, indexY, index_index = mark_finger(frame=frame, finger_point=8, color=colours.BLACK)
                middleX, middleY, middle_index = mark_finger(frame=frame, finger_point=12, color=colours.BLUE)
                ringX, ringY, ring_index = mark_finger(frame=frame, finger_point=16, color=colours.PINK)
                pinkyX, pinkyY, pinky_index = mark_finger(frame=frame, finger_point=20, color=colours.GREEN) 
                
                cursor_position = pyautogui.position()

                if is_fist(thumb=thumb_index, index=index_index, middle=middle_index, ring=ring_index, pinky=pinky_index):
                    cv.putText(frame, "CLICK", (50,50), cv.FONT_HERSHEY_SIMPLEX, 1, colours.GREEN, 2, cv.LINE_AA)                   
                    pyautogui.click()
                    
                elif is_touched(thumb_index, index_index, 4):
                    cv.putText(frame, "UP", (50,50), cv.FONT_HERSHEY_SIMPLEX, 1, colours.GREEN, 2, cv.LINE_AA)
                    pyautogui.moveTo(cursor_position.x,cursor_position.y-30, duration=0.05)

                elif is_touched(middle_index, thumb_index, 4):
                    cv.putText(frame, "DOWN", (50,50), cv.FONT_HERSHEY_SIMPLEX, 1, colours.GREEN, 2, cv.LINE_AA)
                    pyautogui.moveTo(cursor_position.x,cursor_position.y+30, duration=0.05)

                elif is_touched(ring_index, thumb_index, 4):
                    cv.putText(frame, "LEFT", (50,50), cv.FONT_HERSHEY_SIMPLEX, 1, colours.GREEN, 2, cv.LINE_AA)
                    pyautogui.moveTo(cursor_position.x-30,cursor_position.y, duration=0.05)

                elif is_touched(pinky_index, thumb_index, 4):
                    cv.putText(frame, "RIGHT", (50,50), cv.FONT_HERSHEY_SIMPLEX, 1, colours.GREEN, 2, cv.LINE_AA)
                    pyautogui.moveTo(cursor_position.x+30,cursor_position.y, duration=0.05)

            # Uncomment this block to print a label that indicate the shown hand
            """ # Check left or right hand
            who = is_left_or_right(0.5)
            if who == "Right":
                cv.putText(frame, "RIGHT HAND", (430,100), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv.LINE_AA)               
            elif who == "Left":
                cv.putText(frame, "LEFT HAND", (50,100), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv.LINE_AA) """              

    # Show debug window
    if not args["nodebug"]:
        cv.imshow("Camera", frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv.destroyAllWindows()
