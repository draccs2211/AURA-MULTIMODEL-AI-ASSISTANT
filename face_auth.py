import cv2
import face_recognition
import time
import os
import numpy as np
from PIL import Image

def face_authenticate(timeout=30, image_path="C:\\Users\\hp\\OneDrive\\Desktop\\PYTHON\\voice ACTIVE JARVIS\\bsw.jpg", speak=None):
    print("📷 Starting face authentication...")

    if not os.path.exists(image_path):
        print("❌ Image file not found!")
        return False

    try:
        pil_image = Image.open(image_path).convert("RGB")
        known_image = np.array(pil_image).astype(np.uint8)
    except Exception as e:
        print(f"❌ Error loading image: {e}")
        return False

    known_encoding_list = face_recognition.face_encodings(known_image)
    if not known_encoding_list:
        print("❌ No face found in the known image!")
        return False

    known_encoding = known_encoding_list[0]

    # Use DirectShow backend on Windows
    video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not video.isOpened():
        print("❌ Error: Could not access the webcam.")
        return False

    # Warm up the camera
    for _ in range(10):
        video.read()
        time.sleep(0.05)

    print("✅ Webcam opened successfully.")
    print("🕵️ Scanning for your face for 30 seconds...")

    # Ensure the window appears
    window_name = "Face Authentication (Press Q to Cancel)"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.moveWindow(window_name, 100, 100)  # Make sure window is visible

    start_time = time.time()

    while time.time() - start_time < timeout:
        ret, frame = video.read()
        if not ret:
            print("❌ Failed to grab frame from webcam.")
            continue

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding in face_encodings:
            distance = face_recognition.face_distance([known_encoding], face_encoding)[0]
            match = face_recognition.compare_faces([known_encoding], face_encoding, tolerance=0.5)[0]
            print(f"🔍 Face detected. Distance: {distance:.3f} | Match: {match}")

            if match:
                print("✅ Face authenticated successfully.")
                if speak:
                    speak("HELLO DIVYANSH")
                video.release()
                cv2.destroyAllWindows()
                cv2.waitKey(1)  # Ensures window is closed
                return True

        cv2.imshow(window_name, frame)

        # Keeps window responsive
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("⛔ Face authentication cancelled by user.")
            break

    video.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    print("⏱️ Timeout. No match found.")
    return False

# Run directly for testing
if __name__ == "__main__":
    face_authenticate()
