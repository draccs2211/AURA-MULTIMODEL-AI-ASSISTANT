import tkinter as tk
from apis.llm_api import ask_llm

class ChatPanel:
    def __init__(self, root):
        self.frame = tk.Frame(root, bg="#1e1e1e")
        self.frame.pack(side="right", fill="both", expand=True)

        self.chat_area = tk.Text(self.frame, bg="#1e1e1e", fg="white", wrap="word")
        self.chat_area.pack(fill="both", expand=True)

        self.entry = tk.Entry(self.frame, bg="#2e2e2e", fg="white")
        self.entry.pack(fill="x")

        self.entry.bind("<Return>", self.send_message)

    def send_message(self, event=None):
        user_text = self.entry.get().strip()
        if not user_text:
            return
        
        self.chat_area.insert(tk.END, f"\n🧑 YOU: {user_text}\n")
        self.entry.delete(0, tk.END)

        response = ask_llm(user_text)
        self.chat_area.insert(tk.END, f"🤖 AURA: {response}\n")
