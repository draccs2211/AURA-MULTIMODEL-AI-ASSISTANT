import tkinter as tk
from tkinter import scrolledtext
import requests

# Minimal LLM (replace later with OpenAI/Groq/Gemini)
def ask_llm(prompt):
    # Temporary mock response
    return f"You said: {prompt}"

class ChatPanel:
    def __init__(self, root):
        container = tk.Frame(root, bg="#121212")
        container.pack(side="right", fill="both", expand=True)

        tk.Label(container, text="AURA CHAT", bg="#121212", fg="white",
                 font=("Arial", 16)).pack(pady=10)

        self.chat_area = scrolledtext.ScrolledText(
            container, wrap="word",
            bg="#1e1e1e", fg="white", font=("Arial", 12)
        )
        self.chat_area.pack(fill="both", expand=True)

        self.entry = tk.Entry(container, bg="#2c2c2c", fg="white",
                              font=("Arial", 13))
        self.entry.pack(fill="x")
        self.entry.bind("<Return>", self.send_message)

    def send_message(self, event=None):
        user_text = self.entry.get().strip()
        if not user_text:
            return

        # Display user message
        self.chat_area.insert(tk.END, f"\n🧑 YOU: {user_text}\n")
        self.entry.delete(0, tk.END)

        # LLM Response
        response = ask_llm(user_text)

        # Display AURA response
        self.chat_area.insert(tk.END, f"🤖 AURA: {response}\n")
