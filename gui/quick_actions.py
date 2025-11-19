import tkinter as tk
import webbrowser
from utils.speak import speak  # If you don't want this, remove speak()

class QuickActions:
    def __init__(self, parent):
        frame = tk.Frame(parent, bg="#1c1c1c")
        frame.pack(fill="x", pady=10)

        tk.Label(frame, text="QUICK ACTIONS", bg="#1c1c1c",
                 fg="white", font=("Arial", 16)).pack()

        tk.Button(frame, text="Open Google", command=self.open_google,
                  bg="#2b2b2b", fg="white", width=20).pack(pady=5)

        tk.Button(frame, text="Weather Report",
                  command=lambda: speak("Fetching weather"),
                  bg="#2b2b2b", fg="white", width=20).pack(pady=5)

        tk.Button(frame, text="Latest News",
                  command=lambda: speak("Fetching news"),
                  bg="#2b2b2b", fg="white", width=20).pack(pady=5)

    def open_google(self):
        speak("Opening Google")
        webbrowser.open("https://google.com")
