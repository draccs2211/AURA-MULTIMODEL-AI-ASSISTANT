
import cv2
import mediapipe as mp
import threading
import time
import os
import subprocess
import pygetwindow as gw
import win32gui
import numpy as np
from math import hypot
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import screen_brightness_control as sbc
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from google.protobuf.json_format import MessageToDict

# MediaPipe setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

should_exit = False
last_global_gesture_time = 0

# Volume setup
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volMin, volMax = volume.GetVolumeRange()[:2]

# ---- Detect finger state ----
def count_fingers(hand_landmarks):
    fingers = []
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    tips = [8, 12, 16, 20]
    for tip in tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers

# ---- Recognize gesture ----
def recognize_gesture(fingers):
    if fingers == [0, 1, 1, 0, 0]:
        return "two_fingers"
    elif fingers == [0, 0, 0, 0, 0]:
        return "fist"
    elif fingers == [1, 1, 1, 1, 1]:
        return "open_palm"
    elif fingers == [0, 1, 0, 0, 0]:
        return "point"
    elif fingers == [0, 1, 1, 1, 1]:
        return "rock_on"
    elif fingers == [0, 0, 0, 0, 1]:
        return "finger_down"
    elif fingers == [0, 1, 1, 1, 0]:
        return "two_finger_swipe"
    else:
        return "unknown"

# ---- Handle right hand gesture ----
def handle_gesture(gesture):
    global should_exit, last_global_gesture_time
    from jarvis import speak, get_weather
    import jarvis

    now = time.time()
    if now - last_global_gesture_time < 3:
        return
    last_global_gesture_time = now

    try:
        if gesture == "open_palm":
            def minimize_active_window():
                try:
                    hwnd = win32gui.GetForegroundWindow()
                    win32gui.ShowWindow(hwnd, 6)
                    print("Window minimized.")
                except Exception as e:
                    print("Error minimizing window:", e)
            minimize_active_window()

        elif gesture == "two_fingers":
            threading.Thread(target=speak, args=("Opening VS Code.",)).start()
            subprocess.Popen([r"C:\\Users\\hp\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"])

        elif gesture == "fist":
            threading.Thread(target=speak, args=("EXITING GESTURE MODE.",)).start()
            should_exit = True

        elif gesture == "rock_on":
            threading.Thread(target=speak, args=("Launching Spotify.",)).start()
            subprocess.Popen(["C:\\Users\\hp\\AppData\\Roaming\\Spotify\\Spotify.exe"])

        elif gesture == "finger_down":
            threading.Thread(target=speak, args=("Minimizing all windows.",)).start()
            subprocess.Popen(['powershell', '-command', '(new-object -com shell.application).minimizeall()'])

        elif gesture == "point":
            notes_path = "C:\\Users\\hp\\OneDrive\\Desktop\\PYTHON\\voice ACTIVE JARVIS\\notes.txt"
            threading.Thread(target=speak, args=("Opening your notes.",)).start()
            os.system(f'start notepad "{notes_path}"')

        elif gesture == "two_finger_swipe":
            threading.Thread(target=get_weather).start()

    except Exception as e:
        print(f"❌ Error while handling gesture '{gesture}': {e}")

# ---- Gesture loop ----
def gesture_loop():
    global should_exit

    cap = cv2.VideoCapture(0)
    hands = mp_hands.Hands(min_detection_confidence=0.75)
    last_gesture = None
    last_time = 0
    cooldown = 3

    while True:
        if should_exit:
            break

        success, img = cap.read()
        img = cv2.flip(img, 1)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        left_list, right_list = [], []
        right_hand_gesture = None

        if results.multi_hand_landmarks and results.multi_handedness:
            for idx, hand_handedness in enumerate(results.multi_handedness):
                label = MessageToDict(hand_handedness)['classification'][0]['label']
                hand_landmarks = results.multi_hand_landmarks[idx]

                h, w, _ = img.shape
                landmarks = [[int(lm.x * w), int(lm.y * h)] for lm in hand_landmarks.landmark]

                if label == 'Left':
                    left_list = landmarks
                elif label == 'Right':
                    right_list = landmarks

                mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                fingers = count_fingers(hand_landmarks)
                gesture = recognize_gesture(fingers)
                current_time = time.time()

                if label == 'Right' and gesture != "unknown":
                    if gesture != last_gesture or (current_time - last_time > cooldown):
                        print(f"✋ Right Hand Gesture Detected: {gesture}")
                        threading.Thread(target=handle_gesture, args=(gesture,)).start()
                        last_gesture = gesture
                        last_time = current_time

        # Left Hand Brightness and Volume Control (only if right hand is not active)
        if left_list and not right_list:
            thumb_tip = left_list[4]
            index_tip = left_list[8]
            wrist = left_list[0]
            index_base = left_list[5]

            # Brightness Up - Thumbs Up
            if thumb_tip[1] < wrist[1] and thumb_tip[1] < index_base[1]:
                sbc.set_brightness(min(sbc.get_brightness()[0] + 10, 100))
                cv2.putText(img, "Brightness Up", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # Brightness Down - Thumbs Down
            elif thumb_tip[1] > wrist[1] and thumb_tip[1] > index_base[1]:
                sbc.set_brightness(max(sbc.get_brightness()[0] - 10, 0))
                cv2.putText(img, "Brightness Down", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            # Volume control - Thumb and Index Distance
            else:
                length = hypot(index_tip[0] - thumb_tip[0], index_tip[1] - thumb_tip[1])
                cv2.line(img, index_tip, thumb_tip, (0, 0, 255), 3)
                vol = np.interp(length, [15, 200], [volMin, volMax])
                volume.SetMasterVolumeLevel(vol, None)
                vol_display = int(np.interp(length, [15, 160], [0, 100]))
                cv2.putText(img, f"Volume: {vol_display}%", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                cv2.putText(img, f"Length: {int(length)}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)


        # UI
        remaining = max(0, round(3 - (time.time() - last_global_gesture_time), 1))
        cv2.putText(img, f"Cooldown: {remaining}s", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow("Gesture Recognition", img)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    print("👋 Gesture control loop exited.")

if __name__ == "__main__":
    gesture_loop()

