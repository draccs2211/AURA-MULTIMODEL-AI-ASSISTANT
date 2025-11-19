import tkinter as tk

class StatusPanel:
    def __init__(self, parent):
        frame = tk.Frame(parent, bg="#1c1c1c")
        frame.pack(fill="x", pady=10)

        tk.Label(frame, text="STATUS", fg="white", bg="#1c1c1c",
                 font=("Arial", 16)).pack()

        self.voice_status = tk.Label(frame, text="Voice: ACTIVE",
                                     bg="#1c1c1c", fg="lightgreen")
        self.voice_status.pack(pady=5)

        self.gesture_status = tk.Label(frame, text="Gesture: RUNNING",
                                       bg="#1c1c1c", fg="lightgreen")
        self.gesture_status.pack(pady=5)

        self.face_status = tk.Label(frame, text="Face Auth: VERIFIED",
                                    bg="#1c1c1c", fg="lightgreen")
        self.face_status.pack(pady=5)
