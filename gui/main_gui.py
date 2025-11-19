import tkinter as tk
from gui.chat_panel import ChatPanel
from gui.status_panel import StatusPanel
from gui.quick_actions import QuickActions
from gui.logs_panel import LogsPanel


class AuraGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AURA AI CONTROL CENTER")
        self.root.geometry("1200x700")
        self.root.configure(bg="#121212")

        # LEFT SECTION (Status + Quick Actions + Logs)
        left_frame = tk.Frame(self.root, bg="#1c1c1c", width=350)
        left_frame.pack(side="left", fill="y")

        self.status_panel = StatusPanel(left_frame)
        self.quick_actions = QuickActions(left_frame)
        self.logs_panel = LogsPanel(left_frame)

        # RIGHT SECTION (Chat Panel)
        self.chat_panel = ChatPanel(self.root)

    def run(self):
        self.root.mainloop()
