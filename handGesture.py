import cv2
import mediapipe as mp
import os
import subprocess
import time

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils

finger_tips = [8, 12, 16, 20]
thumb_tip = 4
cap = cv2.VideoCapture(0)
prev_fingers = -1
cooldown = 3  
last_action_time = 0

def count_fingers(hand_landmarks):
    fingers = []

    
    if hand_landmarks.landmark[thumb_tip].x < hand_landmarks.landmark[thumb_tip - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    
    for tip in finger_tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers.count(1)

def launch_app(finger_count):
    if finger_count == 1:
        subprocess.Popen(['notepad.exe'])
        print("Launching Notepad")
    elif finger_count == 2:
        subprocess.Popen('start microsoft.windows.camera:', shell=True)
        print("Launching Camera")
    elif finger_count == 3:
        subprocess.Popen(['calc.exe'])
        print("Launching Calculator")
    elif finger_count == 4:
        subprocess.Popen("start cmd", shell=True)
        print("Launching Command Prompt")
    elif finger_count == 5:
        print("Exiting...")
        cap.release()
        cv2.destroyAllWindows()
        exit()

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            finger_count = count_fingers(handLms)

            
            if finger_count != prev_fingers and time.time() - last_action_time > cooldown:
                launch_app(finger_count)
                prev_fingers = finger_count
                last_action_time = time.time()

            cv2.putText(img, f'Fingers: {finger_count}', (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Hand Gesture App Launcher", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
