import tkinter as tk
from tkinter import scrolledtext

class LogsPanel:
    def __init__(self, parent):
        frame = tk.Frame(parent, bg="#1c1c1c")
        frame.pack(fill="both", expand=True, pady=10)

        tk.Label(frame, text="LOGS", bg="#1c1c1c",
                 fg="white", font=("Arial", 16)).pack()

        self.log_box = scrolledtext.ScrolledText(
            frame, height=10, bg="#1e1e1e",
            fg="white", font=("Arial", 10)
        )
        self.log_box.pack(fill="both", expand=True)

    def add_log(self, text):
        self.log_box.insert(tk.END, f"{text}\n")
        self.log_box.see(tk.END)
